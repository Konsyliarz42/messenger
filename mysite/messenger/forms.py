from django import forms
from django.core.validators import validate_email, EmailValidator
from django.core.exceptions import ValidationError

from .models import User

MESSAGES = {
    'error': {
        'username_exist': "This username is already used.",
        'username_found': "User has not found.",
        'username_short': "The username must have min. 3 marks.",
        'email_invalid': "This is not an address e-mail.",
        'email_exist': "This email is already used.",
        'password_confirm': "Write two the same passwords.",
        'password_required': "The password is required.",
        'password_short': "The password must have min. 8 marks",
        'password_wrong': "Wrong password."
    }
}

class RegisterForm(forms.ModelForm):
    
    class Meta:

        model = User
        fields = [
            'username',
            'email',
            'password'
        ]
        widgets = {
            'password': forms.PasswordInput,
            'email': forms.EmailInput
        }
        help_texts = {
            'username': ""
        }

    email = forms.EmailField(error_messages={'invalid': MESSAGES['error']['email_invalid']})
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):

        cleaned_data = super(RegisterForm, self).clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', MESSAGES['error']['password_confirm'])

        if len(password) < 8:
            self.add_error('password', MESSAGES['error']['password_short'])

        if User.objects.filter(email=email).all():
            self.add_error('email', MESSAGES['error']['email_exist'])

        if User.objects.filter(username=username).all():
            self.add_error('username', MESSAGES['error']['username_exist'])

        if len(username) < 3:
            self.add_error('username', MESSAGES['error']['username_short'])

        
class LoginForm(forms.Form):

    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150, widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)

    def clean(self):

        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        user = User.objects.filter(username=username).all()

        if not user:
            self.add_error('username', MESSAGES['error']['username_found'])
        else:
            user = user[0]

            if not user.check_password(password):
                self.add_error('password', MESSAGES['error']['password_wrong'])


class EditProfileForm(forms.Form):

    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(widget=forms.EmailInput, error_messages={'invalid': MESSAGES['error']['email_invalid']})
    password = forms.CharField(max_length=150, widget=forms.PasswordInput, required=False)
    new_password = forms.CharField(max_length=150, widget=forms.PasswordInput, required=False)
    confirm_new_password = forms.CharField(max_length=150, widget=forms.PasswordInput, required=False)

    def __init__(self, user, *args, **kwargs):
        
        self.user = user
        super(EditProfileForm, self).__init__(*args, **kwargs)
        

    def clean(self):

        cleaned_data = super(EditProfileForm, self).clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')


        if new_password:
            if new_password != confirm_new_password:
                self.add_error('confirm_new_password', MESSAGES['error']['password_confirm'])

            if len(new_password) < 8:
                self.add_error('new_password', MESSAGES['error']['password_short'])

            if not password:
                self.add_error('password', MESSAGES['error']['password_required'])
            elif not self.user.check_password(password):
                self.add_error('password', MESSAGES['error']['password_wrong'])

        if self.user.email != email:
            if User.objects.filter(email=email).all():
                self.add_error('email', MESSAGES['error']['email_exist'])

        if self.user.username != username:
            if User.objects.filter(username=username).all():
                self.add_error('username', MESSAGES['error']['username_exist'])

            if len(username) < 3:
                self.add_error('username', MESSAGES['error']['username_short'])