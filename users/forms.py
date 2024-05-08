from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.mail import send_mail
from users.models import CustomUser
from django.contrib.auth.views import PasswordResetForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password1'])
        user.save()

        # Send email
        # if user.email:
        #     send_mail(
        #         "Welcome to Goodreads Clone",
        #         f"Hi, {user.username}. You have successfully registered. Enjoy the books and reviews.",
        #         "jonibekhamroqulov2004@gmail.com",
        #         [user.email]
        #     )

        return user

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_image']


