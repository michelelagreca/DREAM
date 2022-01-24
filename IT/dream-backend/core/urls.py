from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import MyTokenObtainPairView   # custom implementation of the token response

# link to the application urls files
# configuration of root of navigation

# basically here we provide the entry points for our django applications

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('forum.urls', namespace='forum')),
    path('api/', include('forum_api.urls', namespace='forum_api')),

    # path('', include('report.urls', namespace='report')),
    path('api/report', include('report_api.urls', namespace='report_api')),

    # This is the endpoint to connect to user app
    path('api/user/', include('users.urls', namespace='users')),

    # This are the endpoints to get the tokens
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

