from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from forum.models import Question, Category, Tip, Answer
from .serializers import AnswerDislikeSerializer, AnswerLikeSerializer, QuestionSerializer, CategorySerializer, \
    TipDislikeSerializer, TipLikeSerializer, TipSerializer, AnswerSerializer, TipVoteSerializer
from django.db.models import F


# import here all the needed DB models
# from forum.models import MODEL_NAME

# import serializers fro each model, they are needed to create the endpoints
# from .serializers import SERIALIZER_NAME


# ADD HERE GENERIC VIEW FOR DEBUGGING PORPOUSE, THEY ARE INCLUDED IN THE REST FRAMEWORK

class CategoryList(generics.ListAPIView):
    queryset = Category.categoryobjects.all()
    serializer_class = CategorySerializer


# GET -> list all categories


class QuestionList(generics.ListCreateAPIView):
    queryset = Question.questionobjects.all()
    serializer_class = QuestionSerializer


# GET -> list all questions
# POST -> inserts a question

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


# GET + parameter-> retireve a question
# PUT + parameter-> update the question denoted by the parameter
# DELETE + parameter-> delete the question denoted by the parameter


class TipList(generics.ListCreateAPIView):
    queryset = Tip.tipobjects.all()
    serializer_class = TipSerializer


# GET -> list all tips
# POST -> inserts a tips

class TipDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tip.objects.all()
    serializer_class = TipSerializer


# GET + parameter-> retireve a tip
# PUT + parameter-> update the tip denoted by the parameter
# DELETE + parameter-> delete the tip denoted by the parameter

class AnswerList(generics.ListCreateAPIView):
    queryset = Answer.answerobjects.all()
    serializer_class = AnswerSerializer


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


# my trial
class TipVote(generics.RetrieveUpdateDestroyAPIView):
    # querysetRaw = Tip.objects.all()
    pass


# https://www.django-rest-framework.org/api-guide/requests/
# DOC django rest HTTP: https://www.django-rest-framework.org/tutorial/2-requests-and-responses/

# allow only POST
@api_view(['POST'])
def tip_like(request):
    # pass http request data to custom serializer
    tip_serializer = TipVoteSerializer(data=request.data)

    # check validation
    if not tip_serializer.is_valid():
        return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)

    # how to read validated data
    tip_id = tip_serializer.validated_data["tip_id"]
    is_like = tip_serializer.validated_data["is_like"]

    print(f'{tip_id}')
    print(f'{is_like}')

    # how ot access user data
    print(f'auth: {request.auth}')      # access token sender
    print(f'user: {request.user}')      # access user instance sender
    print(f'user group: {request.user.groups}')  # access user instance sender

    """
    example on how to check group permission for users
    def is_in_multiple_groups(user):
        return user.groups.filter(name__in=['group1', 'group2']).exists()
    """
    try:
        tip = Tip.objects.get(pk=tip_id)

    except Tip.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(data="Like sent", status=status.HTTP_200_OK)


class TipLike(generics.RetrieveAPIView):
    queryset = Tip.objects.all()
    serializer_class = TipLikeSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Tip.objects.filter(pk=instance.id).update(likes=F('likes') + 1)
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AnswerLike(generics.RetrieveAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerLikeSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Answer.objects.filter(pk=instance.id).update(likes=F('likes') + 1)
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TipDislike(generics.RetrieveAPIView):
    queryset = Tip.objects.all()
    serializer_class = TipDislikeSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Tip.objects.filter(pk=instance.id).update(dislikes=F('dislikes') + 1)
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AnswerDislike(generics.RetrieveAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerDislikeSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Answer.objects.filter(pk=instance.id).update(dislikes=F('dislikes') + 1)
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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
