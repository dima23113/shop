from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from .models import CustomUser
from .forms import LoginForm, PasswordChangeForm, UserRegisterForm, UserChangeBioForm, UserChangePhoneForm
from django_email_verification import send_email


class UserLoginView(View):

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('shop:index')
        else:
            form = LoginForm()
            return render(request, 'account/login.html', {'form': form})

    def post(self, request, *args, **kwargs):

        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.add_message(request, messages.INFO,
                                         'Успешно!')
                    return redirect('shop:index')
                else:
                    messages.error(request, 'Аккаунт заблокирован')
                    return redirect('account:login')
            else:
                messages.error(request, 'Неверный логин/пароль или аккаунт не активирован!')
                return redirect('account:login')


class UserLogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('shop:index')


class PasswordChangeView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = PasswordChangeForm()
            return render(request, 'account/password_change.html', {'form': form})
        else:
            return redirect('account:login')

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = CustomUser.objects.get(email=request.user)
            if cd['new_password'] == cd['confirm_password']:
                user.password = make_password(cd['new_password'])
                user.save()
                login(request, user)
                return redirect('shop:index')
            else:
                messages.error(request, 'Пароли не совпадают')
                return redirect('account:password_change')


class ProfileView(View):

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(email=request.user)
        form_bio = UserChangeBioForm()
        form_phone = UserChangePhoneForm()
        context = {
            'user': user,
            'form_bio': form_bio,
            'form_phone': form_phone
        }

        return render(request, 'account/user_profile.html', context=context)

    def post(self, request, *args, **kwargs):
        user = CustomUser.objects.get(email=request.user)
        form_bio = UserChangeBioForm(request.POST)
        if form_bio.is_valid():
            cd = form_bio.cleaned_data
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.surname = cd['surname']
            user.save()
            return redirect('account:profile')

        form_phone = UserChangePhoneForm(request.POST)
        if form_phone.is_valid():
            cd = form_phone.cleaned_data
            user.phone = cd['phone']
            user.save()
            return redirect('account:profile')


class UserRegisterView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('shop:index')
        else:
            form = UserRegisterForm()
            return render(request, 'account/register.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password'] != cd['confirm_password']:
                messages.error(request, 'Пароли не совпадают!')
                return redirect('account:register')
            elif CustomUser.objects.filter(email=cd['email']).exists():
                messages.error(request, 'Пользователь с таким email существует!')
                return redirect('account:register')
            else:
                user = CustomUser.objects.create_user(email=cd['email'], password=cd['password'])
                user.is_active = False
                send_email(user)
                messages.add_message(request, messages.INFO,
                                     'Вам на почту отправлено письмо с подтвержением регистрациии!')
                return redirect('shop:index')


class PasswordResetView(View):

    def get(self, request, *args, **kwargs):
        form = PasswordResetForm()
        return render(request, 'account/password_reset.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = CustomUser.objects.filter(email=cd['email']).exists()
            if user:
                user = CustomUser.objects.get(email=cd['email'])
                subject = 'Сброс пароля'
                email_template_name = 'account/password_reset_email.html'
                c = {
                    'email': user.email,
                    'domain': '127.0.0.1:8000',
                    'site_name': 'Website',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Неверный заголовок')
                messages.add_message(request, messages.INFO,
                                     'Вам на почту отправлено письмо с подтвержением сброса пароля')
                return redirect('shop:index')
