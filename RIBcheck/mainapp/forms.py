from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import random, string
from .signature import RIBsignature

digits = list(string.digits)
alph = list(string.ascii_lowercase)

class NewUserForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    adress = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Adress'}))
    country = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Country'}), max_length=3)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2", "adress", "country")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        iban_prefix = "FR76"
        iban_suffix = ''.join(random.choices(digits, k=23))  
        user.iban = iban_prefix + iban_suffix
        user.salt = ''.join(random.choices(digits + alph, k=16))
        user.signature = RIBsignature(str(user.username), str(user.adress), str(user.country), str(user.iban), str(user.salt))
        if commit:
            user.save()
        return user
    
class RIBForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    adress = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Adress'}))
    country = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Country'}), max_length=3)
    iban = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'IBAN'}))