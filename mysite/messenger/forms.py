from django import forms
from django.core.validators import validate_email, EmailValidator
from django.core.exceptions import ValidationError

from .models import User

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

    email = forms.EmailField(error_messages={'invalid': "This is not e-mail."})
    confirm_password = forms.CharField(widget=forms.PasswordInput)


    def clean(self):

        cleaned_data = super(RegisterForm, self).clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', "You have to write two the same passwords.")

        if len(password) < 8:
            self.add_error('password', "Password has to min 8 marks.")

        if User.objects.filter(email=email).all():
            self.add_error('email', "This e-mail is already in our database.")

        if User.objects.filter(username=username).all():
            self.add_error('username', "This username is already in our database.")

        if len(username) < 3:
            self.add_error('username', "Username has to min 3 marks.")

        
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
            self.add_error('username', "We have not founded the user with that name.")
        else:
            user = user[0]

            if not user.check_password(password):
                self.add_error('password', "The password is wrong.")