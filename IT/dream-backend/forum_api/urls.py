from django.urls import path
from .views import QuestionList, QuestionDetail, CategoryList

app_name = 'forum_api' #changed

# we get redirected here from the core
# here we define the application (api in this case) endpoints
urlpatterns = [
    path('posting/question/<int:pk>/', QuestionDetail.as_view(), name='questiondetailcreate'),
    path('posting/question', QuestionList.as_view(), name='questionlistcreate'),
    path('posting/category', CategoryList.as_view(), name='categorylist')
]