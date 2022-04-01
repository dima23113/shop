from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import View
from .forms import CreateTicketForm
from account.models import CustomUser


class CreateTicketView(View):

    def post(self, request, *args, **kwargs):
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(email=request.user)
            ticket = form.save(commit=False)
            ticket.user = user
            ticket.save()
        return redirect('account:tickets')