from django.urls import path
from .views import tip_like, tip_dislike, answer_like, answer_dislike, question_list, tip_list, answer_list, \
    question_add, tip_add, answer_add, tip_remove_vote, answer_remove_vote
from .views import CategoryList
# from .views import TipListArea, TipListCategory

app_name = 'forum_api'  # changed

# we get redirected here from the core
# here we define the application (api in this case) endpoints
urlpatterns = [
    path('categories', CategoryList.as_view(), name='categorylist'),

    path('posting/question/', question_add, name='questioncreate'),
    path('posting/tip/', tip_add, name='tipcreate'),
    path('posting/answer/', answer_add, name='answerlistcreate'),

    path('reading/tips', tip_list, name='tiplistcreate'),
    # path('reading/tip/by-category/<category>', TipListCategory.as_view(), name='tiplistcategory'),
    # path('reading/tip/by-area/<area>', TipListArea.as_view(), name='tiplistarea'),
    path('reading/questions', question_list, name='questionlistcreate'),

    path('voting/tip/like', tip_like, name='tip_like'),
    path('voting/tip/dislike', tip_dislike, name='tip_dislike'),
    path('voting/tip/remove-vote', tip_remove_vote, name='tip_remove_vote'),

    path('voting/answer/like', answer_like, name='answer_like'),
    path('voting/answer/dislike', answer_dislike, name='answer_dislike'),
    path('voting/answer/remove-vote', answer_remove_vote, name='answ_remove_vote'),

    path('reading/answers/', answer_list, name='answer_list')

]
