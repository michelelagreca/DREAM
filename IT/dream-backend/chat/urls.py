from django.urls import path
from .views import hr_message_add, hr_message_list

app_name = 'chat'

urlpatterns = [
    path('send-hr-message/', hr_message_add, name='messagecreate'),
    path('load-hr-messages/', hr_message_list, name='messageload'),
]