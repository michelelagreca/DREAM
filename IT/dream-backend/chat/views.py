from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from chat.models import Message
from .serializers import MessageSerializer
from django.db.models import F

class MessageList(generics.ListCreateAPIView):
    queryset = Message.messageobjects.all()
    serializer_class = MessageSerializer

class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.messageobjects.all()
    serializer_class = MessageSerializer

