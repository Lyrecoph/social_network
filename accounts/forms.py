from django import forms
# from django.contrib.auth.models import User
from accounts.models import CustomUser as User

class UserRegistration(forms.ModelForm):
    password = forms.CharField(label= 'password', widget=forms.PasswordInput)
    password2 = forms.CharField(label= 'Repeat password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        
    def check_username(self):
        cd = self.cleaned_data
        
        if cd['password']!= cd['password2']:
            raise forms.ValidationError("Les mots de passe ne sont pas identiques")
        
        