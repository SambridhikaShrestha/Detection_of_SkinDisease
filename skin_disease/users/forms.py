from django import forms
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'name', 'last_name', 'age']
        widgets = {
            'password': forms.PasswordInput(),
        }