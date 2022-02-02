from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from django.utils import timezone
from core.serializers import IdGeneralSerializer
from forum.models import Question, Category, Tip, Answer
from .serializers import QuestionSerializer, CategorySerializer, TipSerializer, AnswerSerializer, TipVoteSerializer, \
    AnswerVoteSerializer
from django.core import serializers
from django.http import HttpResponse
from django.db.models import F
from django.core.exceptions import PermissionDenied
from rest_framework import permissions

# import here all the needed DB models
# from forum.models import MODEL_NAME

# import serializers fro each model, they are needed to create the endpoints
# from .serializers import SERIALIZER_NAME


class FarmerGroupPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.groups.filter(name = "farmer-group").exists():
        #if not request.user.has_perm('forum.view_answer'):
        # row above is for check direct permissions
            raise PermissionDenied
        return True


class PolicyMakerGroupPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.groups.filter(name = "policymaker-group").exists():
            raise PermissionDenied
        return True



class CategoryList(generics.ListAPIView):
    queryset = Category.categoryobjects.all()
    serializer_class = CategorySerializer


# GET -> list all questions
# POST -> inserts a question

class QuestionDetail(generics.RetrieveAPIView, FarmerGroupPermission):
    permission_classes = [FarmerGroupPermission]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


# GET + parameter-> retireve a question
# PUT + parameter-> update the question denoted by the parameter
# DELETE + parameter-> delete the question denoted by the parameter


class TipList(generics.ListAPIView, FarmerGroupPermission):
    permission_classes = [FarmerGroupPermission]
    serializer_class = TipSerializer

    def get_queryset(self):
        queryset = Tip.objects.all()
        for tip in queryset:
            tip.user_like = False
            tip.user_dislike = False
            if self.request.user in tip.likes.all():
                tip.user_like = True
            if self.request.user in tip.dislikes.all():
                tip.user_dislike = True
        return queryset


# GET -> list all tips

class TipDetail(generics.RetrieveAPIView, FarmerGroupPermission):
    permission_classes = [FarmerGroupPermission]
    queryset = Tip.objects.all()
    serializer_class = TipSerializer


# GET + parameter-> retireve a tip
# PUT + parameter-> update the tip denoted by the parameter
# DELETE + parameter-> delete the tip denoted by the parameter

class TipListCategory(generics.ListAPIView, FarmerGroupPermission):
    permission_classes = [FarmerGroupPermission]
    serializer_class = TipSerializer

    def get_queryset(self):
        category = self.kwargs['category']
        return Tip.objects.filter(category=category)


# GET + category-> retireve a tip of a specific category


class TipListArea(generics.ListAPIView, FarmerGroupPermission):
    permission_classes = [FarmerGroupPermission]
    serializer_class = TipSerializer

    def get_queryset(self):
        area = self.kwargs['area']
        return Tip.objects.filter(area=area)


# GET + area-> retireve a tip of a specific area


class AnswerList(generics.ListCreateAPIView, FarmerGroupPermission):
    permission_classes = [FarmerGroupPermission]
    queryset = Answer.answerobjects.all()
    serializer_class = AnswerSerializer


# GET -> list all answers
# POST -> inserts a answer


class AnswerDetail(generics.RetrieveAPIView, FarmerGroupPermission):
    permission_classes = [FarmerGroupPermission]
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


# https://www.django-rest-framework.org/api-guide/requests/
# DOC django rest HTTP: https://www.django-rest-framework.org/tutorial/2-requests-and-responses/


# ------------- FORUM READING -------------


@api_view(['GET'])
def question_list(request):
    if not request.user.groups.filter(name = "farmer-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
    qs_dict = Question.objects.values()  # get queryset in dictionary form
    qs = Question.objects.all()  # get queryset as django queryset

    for i in range(len(qs_dict)):  # complete the dictionary with info extracted by the queryset
        answers_dic = Answer.objects.filter(question=qs[i]).values()
        qs_dict[i]['answers_number'] = len(answers_dic)  # count related answers

    return Response(data=qs_dict, status=status.HTTP_200_OK, content_type='application/json')


@api_view(['GET'])
def answer_list(request):
    if not request.user.groups.filter(name = "farmer-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
    question_serializer = IdGeneralSerializer(data=request.GET)

    # check validation
    if not question_serializer.is_valid():
        return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)

    # read validated data
    question_id = question_serializer.validated_data["id"]

    # get answers
    qs = Answer.objects.filter(question_id=question_id)
    qs_dict = Answer.objects.filter(question_id=question_id).values()

    for i in range(len(qs_dict)):  # complete the dictionary with info extracted by the queryset
        qs_dict[i]['user_like'] = False
        qs_dict[i]['user_dislike'] = False

        if request.user in qs[i].likes.all():
            qs_dict[i]['user_like'] = True
        if request.user in qs[i].dislikes.all():
            qs_dict[i]['user_dislike'] = True

        qs_dict[i]['likes'] = len(qs[i].likes.values())
        qs_dict[i]['dislikes'] = len(qs[i].dislikes.values())

    return Response(data=qs_dict, status=status.HTTP_200_OK, content_type='application/json')


@api_view(['GET'])
def tip_list(request):
    if not request.user.groups.filter(name = "farmer-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
    qs_dict = Tip.objects.values()  # get queryset in dictionary form
    qs = Tip.objects.all()  # get queryset as django queryset

    for i in range(len(qs_dict)):  # complete the dictionary with info extracted by the queryset
        qs_dict[i]['user_like'] = False
        qs_dict[i]['user_dislike'] = False

        if request.user in qs[i].likes.all():
            qs_dict[i]['user_like'] = True
        if request.user in qs[i].dislikes.all():
            qs_dict[i]['user_dislike'] = True

        qs_dict[i]['likes'] = len(qs[i].likes.values())
        qs_dict[i]['dislikes'] = len(qs[i].dislikes.values())

    return Response(data=qs_dict, status=status.HTTP_200_OK, content_type='application/json')


# ------------- FORUM POSTING -------------


@api_view(['POST'])
def answer_add(request):
    if not request.user.groups.filter(name = "farmer-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
    # pass http request data to custom serializer
    answer_serializer = AnswerSerializer(data=request.data)

    print(request.data)
    print(answer_serializer.is_valid())
    # prevent anonymous user to access
    if request.user.is_anonymous:
        return Response("Invalid Request", status=status.HTTP_403_FORBIDDEN)

    # check validation
    if not answer_serializer.is_valid():
        return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)

    """try:
        question = Question.objects.get(pk=answer_serializer.validated_data["question"])
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)"""

    # create answer instance
    answer = Answer(
        question=answer_serializer.validated_data["question"],
        author=request.user,
        text_body=answer_serializer.validated_data["text_body"],
    )
    answer.save()

    return Response(data="Answer sent", status=status.HTTP_200_OK)


@api_view(['POST'])
def question_add(request):
    if not request.user.groups.filter(name = "farmer-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
    # pass http request data to custom serializer
    question_serializer = QuestionSerializer(data=request.data)

    # check validation
    if not question_serializer.is_valid():
        return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)

    try:
        category = Category.objects.get(name=question_serializer.validated_data["category"])
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # create question instance
    question = Question(
        title=question_serializer.validated_data["title"],
        text_body=question_serializer.validated_data["text_body"],
        author=request.user,
        category=category,
        area=request.user.area,
    )
    question.save()

    return Response(data="Question sent", status=status.HTTP_200_OK)


@api_view(['POST'])
def tip_add(request):
    if not request.user.groups.filter(name = "farmer-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
    # pass http request data to custom serializer
    tip_serializer = TipSerializer(data=request.data)

    # check validation
    if not tip_serializer.is_valid():
        return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)

    try:
        category = Category.objects.get(pk=tip_serializer.validated_data["category"])
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # create question instance
    tip = Tip(
        title=tip_serializer.validated_data["title"],
        text_body=tip_serializer.validated_data["text_body"],
        author=request.user,
        category=category,
        area=request.user.area,
        is_star=False,
    )
    tip.save()

    return Response(data="Tip posted", status=status.HTTP_200_OK)


# ------------- TIP VOTING -------------

@api_view(['POST'])
def tip_like(request):
    if not request.user.groups.filter(name = "farmer-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
    # pass http request data to custom serializer
    tip_serializer = TipVoteSerializer(data=request.data)

    # check validation
    if not tip_serializer.is_valid():
        return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)

    # how to read validated data
    tip_id = tip_serializer.validated_data["tip_id"]

    try:
        tip = Tip.objects.get(pk=tip_id)
    except Tip.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user in tip.likes.all():
        return Response(data="Like already present", status=status.HTTP_200_OK)

    if request.user in tip.dislikes.all():
        tip.dislikes.remove(request.user)  # remove from dislike relation if present

    tip.likes.add(request.user)
    tip.save()

    return Response(data="Like sent", status=status.HTTP_200_OK)


@api_view(['POST'])
def tip_dislike(request):
    if not request.user.groups.filter(name = "farmer-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
    # pass http request data to custom serializer
    tip_serializer = TipVoteSerializer(data=request.data)

    # check validation
    if not tip_serializer.is_valid():
        return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)

    # how to read validated data
    tip_id = tip_serializer.validated_data["tip_id"]

    try:
        tip = Tip.objects.get(pk=tip_id)
    except Tip.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user in tip.dislikes.all():
        return Response(data="Dislike already present", status=status.HTTP_200_OK)

    if request.user in tip.likes.all():
        tip.likes.remove(request.user)  # remove from like relation if present

    tip.dislikes.add(request.user)
    tip.save()

    return Response(data="DisLike sent", status=status.HTTP_200_OK)


@api_view(['POST'])
def tip_remove_vote(request):
    if not request.user.groups.filter(name = "farmer-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
    # pass http request data to custom serializer
    tip_serializer = TipVoteSerializer(data=request.data)

    # check validation
    if not tip_serializer.is_valid():
        return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)

    # how to read validated data
    tip_id = tip_serializer.validated_data["tip_id"]

    try:
        tip = Tip.objects.get(pk=tip_id)
    except Tip.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user in tip.dislikes.all():
        tip.dislikes.remove(request.user)  # remove from dislike relation if present

    if request.user in tip.likes.all():
        tip.likes.remove(request.user)  # remove from like relation if present

    tip.save()

    return Response(data="DisLike sent", status=status.HTTP_200_OK)


# ------------- ANSWER VOTING -------------

@api_view(['POST'])
def answer_like(request):
    if not request.user.groups.filter(name = "farmer-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
    answer_serializer = AnswerVoteSerializer(data=request.data)

    # validation
    if not answer_serializer.is_valid():
        return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)
    answer_id = answer_serializer.validated_data["answer_id"]

    # db read
    try:
        answer = Answer.objects.get(pk=answer_id)
    except Answer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # db update
    if request.user in answer.likes.all():
        return Response(data="Like already present", status=status.HTTP_200_OK)

    if request.user in answer.dislikes.all():
        answer.dislikes.remove(request.user)  # remove from dislike relation if present

    answer.likes.add(request.user)
    answer.save()

    return Response(data="Like sent", status=status.HTTP_200_OK)


@api_view(['POST'])
def answer_dislike(request):
    if not request.user.groups.filter(name = "farmer-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
    # pass http request data to custom serializer
    answer_serializer = AnswerVoteSerializer(data=request.data)

    # check validation
    if not answer_serializer.is_valid():
        return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)

    # how to read validated data
    answer_id = answer_serializer.validated_data["answer_id"]

    try:
        answer = Answer.objects.get(pk=answer_id)
    except Answer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user in answer.dislikes.all():
        return Response(data="Dislike already present", status=status.HTTP_200_OK)

    if request.user in answer.likes.all():
        answer.likes.remove(request.user)  # remove from like relation if present

    answer.dislikes.add(request.user)
    answer.save()

    return Response(data="DisLike sent", status=status.HTTP_200_OK)


@api_view(['POST'])
def answer_remove_vote(request):
    if not request.user.groups.filter(name = "farmer-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
    # pass http request data to custom serializer
    answer_serializer = AnswerVoteSerializer(data=request.data)

    # check validation
    if not answer_serializer.is_valid():
        return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)

    # how to read validated data
    answer_id = answer_serializer.validated_data["answer_id"]

    try:
        answer = Answer.objects.get(pk=answer_id)
    except Answer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user in answer.dislikes.all():
        answer.dislikes.remove(request.user)  # remove from dislike relation if present

    if request.user in answer.likes.all():
        answer.likes.remove(request.user)  # remove from like relation if present

    answer.save()

    return Response(data="DisLike sent", status=status.HTTP_200_OK)


# GET + parameter-> retireve a answer
# PUT + parameter-> update the answer denoted by the parameter
# DELETE + parameter-> delete the answer denoted by the parameter


class AnswerListQuestion(generics.ListAPIView, FarmerGroupPermission):
    permission_classes = [FarmerGroupPermission]
    serializer_class = AnswerSerializer

    def get_queryset(self):
        question = self.kwargs['question']
        return Answer.objects.filter(question=question)


""" Concrete View Classes
#CreateAPIView
Used for create-only endpoints.
#ListAPIView
Used for read-only endpoints to represent a collection of model instances.
#RetrieveAPIView
Used for read-only endpoints to represent a single model instance.
#DestroyAPIView
Used for delete-only endpoints for a single model instance.
#UpdateAPIView
Used for update-only endpoints for a single model instance.
##ListCreateAPIView
Used for read-write endpoints to represent a collection of model instances.
RetrieveUpdateAPIView
Used for read or update endpoints to represent a single model instance.
#RetrieveDestroyAPIView
Used for read or delete endpoints to represent a single model instance.
#RetrieveUpdateDestroyAPIView
Used for read-write-delete endpoints to represent a single model instance.
"""
