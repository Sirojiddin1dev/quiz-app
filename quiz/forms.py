from django import forms
from customusers.models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator


class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add customizations or additional fields initialization here

    def clean_remember_me(self):
        # Custom clean method for the 'remember_me' field
        # Add your validation logic here
        return self.cleaned_data['remember_me']


class CustomUserCreationForm(UserCreationForm):
    phone_regex = RegexValidator(
        regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', 
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    country = forms.ChoiceField(choices=CustomUser.COUNTRY_CHOICES, widget=forms.RadioSelect)
    phone_number = forms.CharField(validators=[phone_regex], max_length=17, required=False)
    gender = forms.ChoiceField(choices=CustomUser.GENDER_CHOICES, widget=forms.RadioSelect)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'country', 'phone_number', 'gender', 'password1', 'password2')



class LoginForm(forms.Form):
    username = forms.CharField(label="username")
    password = forms.CharField(widget=forms.PasswordInput, label="password")

