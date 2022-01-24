from django.urls import path
from .views import AnswerDetail, AnswerList, QuestionList, QuestionDetail, CategoryList, TipDetail, TipList

app_name = 'forum_api' #changed

# we get redirected here from the core
# here we define the application (api in this case) endpoints
urlpatterns = [
    path('posting/question/<int:pk>/', QuestionDetail.as_view(), name='questiondetailcreate'),
    path('posting/question', QuestionList.as_view(), name='questionlistcreate'),
    path('posting/category', CategoryList.as_view(), name='categorylist'),
    path('posting/tip/<int:pk>/', TipDetail.as_view(), name='tipdetailcreate'),
    path('posting/tip', TipList.as_view(), name='tiplistcreate'),
    #path('voting/tip/like/<int:pk>', TipLike.as_view(), name='tiplike'),
    #path('voting/tip/dislike/<int:pk>', TipDisike.as_view(), name='tipdislike')
    path('posting/answer', AnswerList.as_view(), name='answerlistcreate'),
    path('posting/answer/<int:pk>', AnswerDetail.as_view(), name='answerdetailcreate')
]