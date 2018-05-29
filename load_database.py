# django initialization
# https://stackoverflow.com/questions/39137339/django-exception-django-core-exceptions-improperlyconfigured
import sys, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()

# my imports
from IosVulnCheckApp.models import CiscoDevice
import csv
import re

def main():
    with open('device_list2.csv', 'rb') as f:
        reader = csv.reader(f)
        pattern = re.compile(r'(,\sVersion\s)(.*?)([, ])', re.I)
        pattern2 = re.compile(r'ios.xe', re.I)
        for row in reader:
            m = re.search(pattern, row[1])
            if m:
                #print "%s, %s" % (row[0], m.group(2))
                device, created = CiscoDevice.objects.get_or_create(
                    device_name=row[0]
                )
                device.ios_version = m.group(2)
                n = re.search(pattern2, row[1])
                if n:
                    device.ios_type = "ios-xe"
                    stripped_zero = [i.lstrip('0') for i in device.ios_version]
                    device.ios_version = "".join(stripped_zero)
                else:
                    device.ios_type = "ios"
                device.save()
            else:
                #print "%s, NoMatch" % row[0]
                device, created = CiscoDevice.objects.get_or_create(
                    device_name=row[0]
                )
                device.ios_version = "NoMatch"
                device.ios_type = "unknown"
                device.save()

if __name__ == '__main__':
    main()
