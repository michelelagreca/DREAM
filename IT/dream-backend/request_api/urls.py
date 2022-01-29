from django.urls import path
from .views import RequestList, RequestDetail, send_hr_farmer

app_name = 'request_api'  # changed

# we get redirected here from the core
# here we define the application (api in this case) endpoints
urlpatterns = [
    path('sending_hr_farmer/', send_hr_farmer, name='send_hr_farmer')
]