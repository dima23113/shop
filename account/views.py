from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import *
from .forms import LoginForm


class UserLogin(View):

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
