from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required field')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


def validate_date(value):
    if value is not None:
        return True


class MessageForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField(widget=forms.EmailInput)
    text = forms.CharField(widget=forms.Textarea)
    date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}), localize=True)
