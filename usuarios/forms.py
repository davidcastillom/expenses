from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from registro.models import Profile

# se crea una clase nueva, HEREDANDO de UserCreationForm que viene
#con django, para modificarla
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        # son los campos que se mostraran
        fields = ['username','email','last_login','password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        email = forms.EmailField()
