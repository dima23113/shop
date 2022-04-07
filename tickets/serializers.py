from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Ticket, TicketMessage


class TicketMsgSerializer(ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = ['msg', 'is_admin']


class TicketSerializer(ModelSerializer):
    ticket_msg = TicketMsgSerializer(many=True, read_only=True)
    user = serializers.SlugRelatedField(slug_field='email', read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'
