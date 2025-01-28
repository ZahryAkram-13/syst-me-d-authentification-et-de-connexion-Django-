from django import forms
import re
from .models import Account

import re
from html import escape

def is_valid_login_name(login_name):
    """
    Validates the login name to prevent JavaScript injection and invalid 
    formats.
    
    """
    login_name = login_name.strip()
    
    if re.search(r'<[^>]*script[^>]*>|<[^>]*>', login_name, re.IGNORECASE):
        return False
    
    login_name = escape(login_name)
    
    if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9 _-]*$', login_name):
        return True
    
    return False

class AccountForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = ['login', 'email', 'phone', 'password']

    re_Password = forms.CharField(label = "Confirm Password")

    @staticmethod
    def is_strong_password(password):
        """
        Validates if a password is strong.
        Criteria:
        - At least one uppercase letter
        - At least one number
        - At least one special character
        - Minimum 8 characters in length
        """
        pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        return bool(re.match(pattern, password))

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.is_strong_password(password):
            raise forms.ValidationError(
                "Password must contain at least one uppercase letter, one number, and one special character."
            )
        return password
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not self.valid_phone(phone):
            raise forms.ValidationError(
                "Phone format is not valid"
            )
        return phone
    
    def clean_login(self):
        login = self.cleaned_data.get('login')
        if not is_valid_login_name(login):
            raise forms.ValidationError(
                "suspicious login,  format is not valid"
            )
        return login

    @staticmethod
    def valid_phone(phone):
        pattern = r"^\+\d{1,3}\s[1-9](?:\s\d{2}){4}$"
        return bool(re.match(pattern, phone))
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')
        

        if password and re_password and password != re_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    


class LoginForm(forms.Form):

    #validation required

    email = forms.CharField(label = "email")
    password = forms.CharField(label = "Password",widget=forms.PasswordInput)
