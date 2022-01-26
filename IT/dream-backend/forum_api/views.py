from rest_framework.response import Response
from rest_framework import generics
from forum.models import Question, Category, Tip, Answer
from .serializers import AnswerDislikeSerializer, AnswerLikeSerializer, QuestionSerializer, CategorySerializer, TipDislikeSerializer, TipLikeSerializer, TipSerializer, AnswerSerializer
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

class TipListCategory(generics.ListAPIView):
    serializer_class = TipSerializer

    def get_queryset(self):
        category = self.kwargs['category']
        return Tip.objects.filter(category=category)

# GET + category-> retireve a tip of a specific category


class TipListArea(generics.ListAPIView):
    serializer_class = TipSerializer

    def get_queryset(self):
        area = self.kwargs['area']
        return Tip.objects.filter(area=area)

# GET + area-> retireve a tip of a specific area


class AnswerList(generics.ListCreateAPIView):
    queryset = Answer.answerobjects.all()
    serializer_class = AnswerSerializer

# GET -> list all answers
# POST -> inserts a answer


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

# GET + parameter-> retireve a answer
# PUT + parameter-> update the answer denoted by the parameter
# DELETE + parameter-> delete the answer denoted by the parameter

class AnswerListQuestion(generics.ListAPIView):
    serializer_class = AnswerSerializer

    def get_queryset(self):
        question = self.kwargs['question']
        return Answer.objects.filter(question=question)

# GET + question-> retrieve all answer of a specific question


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