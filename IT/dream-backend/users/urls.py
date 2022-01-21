from django.urls import path
from .views import PostUser

app_name = 'users'

urlpatterns = [
    # registration endpoint
    path('register/', PostUser.as_view(), name='user_create'),
]
