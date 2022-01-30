from django.urls import path
from .views import hr_message_add, hr_message_list, tip_message_add, tip_message_list

app_name = 'chat'

urlpatterns = [
    path('send-hr-message/', hr_message_add, name='hrmessagecreate'),
    path('load-hr-messages/', hr_message_list, name='hrmessageload'),

    path('send-tr-message/', tip_message_add, name='trmessagecreate'),
    path('load-tr-messages/', tip_message_list, name='trmessageload'),
]