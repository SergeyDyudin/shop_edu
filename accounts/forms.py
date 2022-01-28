from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, PasswordResetForm

from accounts.models import CustomUser, Profile, Region

from utils.validators import validate_phone


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
        widgets = {
            'currency': forms.NumberInput(attrs={'readonly': True}),
        }


class AccountForm(forms.ModelForm):
    # region_choices = list(Region.objects.all())
    # region_choices = zip(region_choices, region_choices)
    # region = forms.CharField(widget=forms.Select(choices=region_choices), required=False)
    region = forms.ModelChoiceField(queryset=Region.objects.all(), widget=forms.Select(), required=False)
    phone = forms.CharField(max_length=80, validators=[validate_phone], required=False)
    birthday = forms.DateField(widget=forms.SelectDateWidget(), help_text='Format: MM-DD-YYYY', required=False)
    currency = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly': True}))

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'first_name',
            'last_name',
            'date_joined',
        ]


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


class LoginForm(forms.Form):
    email = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class RegistrationForm(UserCreationForm):
    CHOICES = list(Region.objects.all())
    CHOICES = zip(CHOICES, CHOICES)
    region = forms.CharField(widget=forms.Select(choices=CHOICES), required=False)
    phone = forms.CharField(max_length=80, required=False)
    birthday = forms.DateField(help_text='Required. Format: YYYY-MM-DD', required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'region', 'phone', 'birthday')


class CustomPasswordResetForm(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError("User doesn't exist.")
