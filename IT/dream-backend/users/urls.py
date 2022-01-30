from django.urls import path
from .views import PostUser, BlacklistTokenUpdateView, user_info

app_name = 'users'

urlpatterns = [
    # registration endpoint
    path('register/', PostUser.as_view(), name='user_create'),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist'),

    path('info/', user_info, name='user_info'),
]
