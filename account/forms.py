from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class LoginForm(forms.Form):
    email = forms.EmailField(label='E-Mail', required=True, error_messages={'required': ''})
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль', required=True,
                               error_messages={'required': ''})


class PasswordChangeForm(forms.Form):
    new_password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput, error_messages={'required': ''})
    confirm_password = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput,
                                       error_messages={'required': ''})


class UserRegisterForm(forms.Form):
    email = forms.EmailField(label='E-Mail', required=True, error_messages={'required': ''})
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль', required=True,
                               error_messages={'required': ''})
    confirm_password = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput,
                                       error_messages={'required': ''})


class UserChangeBioForm(forms.Form):
    first_name = forms.CharField(label='Имя', required=True, error_messages={'required': ''})
    last_name = forms.CharField(label='Фамилия', required=True, error_messages={'required': ''})
    surname = forms.CharField(label='Отчество', required=False, error_messages={'required': ''})


class UserChangePhoneForm(forms.Form):
    phone = forms.CharField(label='Номер телефона', required=True, error_messages={'required': ''})

