from django.urls import path
from .views import ReportList, ReportDetail

app_name = 'report_api'

# we get redirected here from the core
# here we define the application (api in this case) endpoints
urlpatterns = [
    path('', ReportList.as_view(), name='reportlist'),
    path('<int:pk>', ReportDetail.as_view(), name='reportdetail'),
]