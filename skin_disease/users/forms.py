import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not re.search(r'[!@#$%^&*()_+=\-[\]{};:\'"|,.<>?]', password1):
            raise forms.ValidationError("Password must contain at least one special character")
        return password1

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@' not in email:
            raise forms.ValidationError("Enter a valid email address")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use")
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Set password using set_password method
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)