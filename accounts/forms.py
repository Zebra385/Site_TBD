from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from accounts.models import CustomUser

class CreatUserForm(UserCreationForm):
    """
    create to use the user of djangoadmin
    """

    class Meta:
        # model = get_user_model()
        model = CustomUser()
        
        fields = UserCreationForm.Meta.fields + ('email', 'username', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nom d\'utilisateur'
        self.fields['email'].label = 'Courriel'

    def save(self, commit=True):
        user = super(CreatUserForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        # make_password to hashe the password
        user.password = make_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """
    Create to login with emai and password
    """
    username = forms.CharField(label='Email / Username')