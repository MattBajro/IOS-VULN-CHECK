# django initialization
# https://stackoverflow.com/questions/39137339/django-exception-django-core-exceptions-improperlyconfigured
import sys, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()

# my imports
from IosVulnCheckApp.models import CiscoDevice, IosVulnerability, VulnMapper
from openVulnQuery import query_client
from requests.exceptions import HTTPError, ConnectionError
import time
import json


def main():
    devs = CiscoDevice.objects.all()
    dev_versions = {}
    for dev in devs:
        dev_versions[dev.ios_version] = dev.ios_type

    # load credentials from file    
    with open('credentials.json', 'r') as f:
        jdata = json.load(f)

    qclient = query_client.OpenVulnQueryClient(
        client_id=jdata['client_id'],
        client_secret=jdata['client_secret']
    )

    progress = 0
    end_progress = len(dev_versions)
    # key => ios version, value => ios/ios-xe
    for key, value in dev_versions.iteritems():
        devs = CiscoDevice.objects.filter(ios_version=key)
        advisories = []
        progress += 1
        print "LOG ::: Progress... %s of %s" % (progress, end_progress)
        successful = False
        if value == 'ios':
            while not successful:
                try:
                    print "LOG ::: Cisco API query for IOS version %s" % (key)
                    advisories = qclient.get_by_ios(key)
                    if len(advisories) > 0:
                        successful = True
                except HTTPError as e:
                    print str(e)
                    print "IOS version %s not found in Cisco PRIST API for:\n%s" % (key, devs)
                    break
                except ConnectionError as e:
                    print str(e)
                    print "LOG ::: Sleeping for 30secs and then retrying..."
                    time.sleep(30)
                    continue
        if value == 'ios-xe':
            while not successful:
                try:
                    print "LOG ::: Cisco API query for IOS-XE version %s" % (key)
                    advisories = qclient.get_by_ios_xe(key)
                    if len(advisories) > 0:
                        successful = True
                except HTTPError as e:
                    print str(e)
                    print "IOS-XE version %s not found in Cisco PRIST API for:\n%s" % (key, devs)
                    break
                except ConnectionError as e:
                    print str(e)
                    print "LOG ::: Sleeping for 30secs and then retrying..."
                    time.sleep(30)
                    continue
        if len(advisories) > 0:
            for adv in advisories:
                vuln_db, created = IosVulnerability.objects.get_or_create(
                    cisco_id=adv.advisory_id
                )
                vuln_db.title = adv.advisory_title
                vuln_db.url = adv.publication_url
                vuln_db.description = adv.summary
                vuln_db.severity = adv.sir
                vuln_db.save()

                for dev in devs:
                    vuln_map, created = VulnMapper.objects.get_or_create(
                        device=dev,
                        vulnerab=vuln_db
                    )
                    if True: #created:
                        vuln_map.ios_version = key
                        vuln_map.affecting = True
                        vuln_map.save()
        time.sleep(10)


if __name__ == '__main__':
    main()
