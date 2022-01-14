from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from .models import CustomUser
from .forms import LoginForm, PasswordChangeForm


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
                    return redirect('shop:index')
                else:
                    messages.error(request, 'Аккаунт заблокирован')
                    return redirect('account:login')
            else:
                messages.error(request, 'Неверный логин или пароль')
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
        context = {
            'user': user
        }

        return render(request, 'account/user_profile.html', context=context)
