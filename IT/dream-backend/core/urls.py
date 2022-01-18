from django.contrib import admin
from django.urls import path, include

# link to the application urls files
# configuration of root of navigation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('forum.urls', namespace='forum')),
    path('api/', include('forum_api.urls', namespace='forum_api'))
]
