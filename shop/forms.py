from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    company_name = forms.CharField(required=False)
    country = forms.CharField(required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "company_name", "country", "avatar"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "username": "Username",
            "email": "Email",
            "password1": "Password",
            "password2": "Confirm Password",
            "company_name": "Company Name (optional)",
            "country": "Country (optional)",
        }
        for name, field in self.fields.items():
            if name in placeholders:
                field.widget.attrs["placeholder"] = placeholders[name]
            field.label = ""
            field.help_text = ""

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Username"
        self.fields["password"].widget.attrs["placeholder"] = "Password"
        self.fields["username"].label = ""
        self.fields["password"].label = ""

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "company_name", "country", "phone", "address"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "company_name": "Company Name",
            "country": "Country",
            "phone": "Phone Number",
            "address": "Business Address",
        }
        for name, field in self.fields.items():
            if name in placeholders:
                field.widget.attrs["placeholder"] = placeholders[name]
            field.label = ""
        self.fields["avatar"].widget.attrs.update({"id": "avatar-real-input", "class": "avatar-real-input", "accept": "image/*"})
