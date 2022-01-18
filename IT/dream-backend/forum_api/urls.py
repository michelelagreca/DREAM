from django.urls import path
from .views import PostList, PostDetail

app_name = 'blog_api'

# we get redirected here from the core
# here we define the application (api in this case) endpoints
urlpatterns = [
    path('<int:pk>/', PostDetail.as_view(), name='detailcreate'),
    path('', PostList.as_view(), name='listcreate'),
]