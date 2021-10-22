from django import forms
from django.contrib.auth import get_user_model

class RegistrationForm(forms.Form):
    username = forms.CharField(label = "Username")
    password = forms.CharField(label = "Password", widget = forms.PasswordInput)
    password2 = forms.CharField(label = "Please repeat your password", widget = forms.PasswordInput)
    email = forms.EmailField(label = "E-Mail-Adress")

    def clean(self):
        cleaned_data = self.cleaned_data
        print(cleaned_data)
        return cleaned_data

    def clean_password2(self):
        cleaned_data = self.cleaned_data
        print(self.cleaned_data)
        password = cleaned_data.get("password")
        print(password)
        password2 = cleaned_data.get("password2")
        print(password2)
        if password != password2 :
            raise forms.ValidationError("Passwords don't match")
        if len(password2)< 8 :
            raise forms.ValidationError("The password is to short - please use more than 8 signs")
        return password2


