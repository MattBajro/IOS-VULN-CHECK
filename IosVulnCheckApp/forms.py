from django import forms

class UpdateDeviceDbForm(forms.Form):
    passphrase = forms.CharField(max_length=50)
