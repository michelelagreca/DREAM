from django.urls import path
from .views import MessageList, MessageDetail

app_name = 'chat'

urlpatterns = [
    path('chat/message/<int:pk>/', MessageDetail.as_view(), name='messagedetailcreate'),
    path('chat/message', MessageList.as_view(), name='messagelistcreate'),
]