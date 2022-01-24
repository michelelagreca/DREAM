from django.urls import path
from .views import RequestList, RequestDetail

app_name = 'blog_api'

# we get redirected here from the core
# here we define the application (api in this case) endpoints
urlpatterns = [
    path('<int:pk>/', RequestDetail.as_view(), name='detailcreate'),
    path('', RequestList.as_view(), name='listcreate'),
]