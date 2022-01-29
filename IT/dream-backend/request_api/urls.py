from django.urls import path
from .views import RequestList, RequestDetail, send_hr_farmer, hr_list_farmer, change_status_hr_farmer

app_name = 'request_api'  # changed

# we get redirected here from the core
# here we define the application (api in this case) endpoints
urlpatterns = [
    path('sending_hr_farmer/', send_hr_farmer, name='send_hr_farmer'),
    path('all_hr/', hr_list_farmer, name='read_hr_farmer'),
    path('changing_status_hr_farmer/', change_status_hr_farmer, name='change_status_hr_farmer'),

]
