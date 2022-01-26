from django.urls import path
from .views import AnswerDetail, AnswerLike, AnswerList, AnswerListQuestion, QuestionList, QuestionDetail, CategoryList, TipDetail, TipLike, TipList, TipDislike, AnswerDislike, TipListArea, TipListCategory

app_name = 'forum_api' #changed

# we get redirected here from the core
# here we define the application (api in this case) endpoints
urlpatterns = [
    path('posting/category', CategoryList.as_view(), name='categorylist'),

    path('posting/question/<int:pk>/', QuestionDetail.as_view(), name='questiondetailcreate'),
    path('posting/question', QuestionList.as_view(), name='questionlistcreate'),

    path('posting/tip/<int:pk>/', TipDetail.as_view(), name='tipdetailcreate'),
    path('posting/tip', TipList.as_view(), name='tiplistcreate'),
    path('posting/tip/by-category/<category>', TipListCategory.as_view(), name='tiplistcategory'),
    path('posting/tip/by-area/<area>', TipListArea.as_view(), name='tiplistarea'),

    path('posting/answer', AnswerList.as_view(), name='answerlistcreate'),
    path('posting/answer/<int:pk>', AnswerDetail.as_view(), name='answerdetailcreate'),
    path('posting/answer/by-question/<question>', AnswerListQuestion.as_view(), name='answerlistquestion'),

    path('voting/tip/<int:pk>/like', TipLike.as_view(), name='tiplike'),
    path('voting/tip/<int:pk>/dislike', TipDislike.as_view(), name='tipdislike'),
    path('voting/answer/<int:pk>/like', AnswerLike.as_view(), name='answerlike'),
    path('voting/answer/<int:pk>/dislike', AnswerDislike.as_view(), name='answerdislike')
    
]