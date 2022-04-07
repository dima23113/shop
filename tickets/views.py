from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import View
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.viewsets import ViewSet, mixins, GenericViewSet

from .forms import CreateTicketForm
from .models import Ticket
from .serializers import TicketSerializer
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


class TicketAPIView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
                    mixins.DestroyModelMixin, GenericViewSet):
    serializer_class = TicketSerializer

    def get_queryset(self):
        queryset = Ticket.objects.select_related('user').prefetch_related('ticket_msg').all()
        return queryset
