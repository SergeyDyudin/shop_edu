from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from accounts.models import CustomUser, Profile


class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = [
            'currency'
        ]


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class SendEmailForm(forms.ModelForm):

    subject = forms.CharField(label='Subject')
    body = forms.CharField(widget=forms.Textarea, label='Text')

    class Meta:
        model = CustomUser
        fields = [
            'email',
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': True}),
        }

    def _get_validation_exclusions(self):
        exclude = super()._get_validation_exclusions()
        exclude.append('email')
        return exclude
