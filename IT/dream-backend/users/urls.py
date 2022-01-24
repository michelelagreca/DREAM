from django.urls import path
from .views import PostUser, BlacklistTokenUpdateView

app_name = 'users'

urlpatterns = [
    # registration endpoint
    path('register/', PostUser.as_view(), name='user_create'),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist')
]
