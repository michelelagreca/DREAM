from rest_framework import serializers
from forum.models import Question, Category, Tip, Answer


# Serializers are used to bind routes together with data from the DB
# they also specify the (JSON) shape of the data provided to the callers
# DOC serializers: https://www.django-rest-framework.org/api-guide/serializers/


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)
    


class QuestionSerializer(serializers.ModelSerializer):
    # category = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ('id', 'title', 'text_body', 'category')

    # def get_category(self, category):
    #       return category.category.name 
    # this was to show the name of the category in the json, instead of the number referring the id


# custom serializer to handle post json of vote request
class TipVoteSerializer(serializers.Serializer):
    tip_id = serializers.IntegerField()


class AnswerVoteSerializer(serializers.Serializer):
    answer_id = serializers.IntegerField()


class TipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tip
        fields = ('id', 'title', 'text_body', 'category')


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('question', 'text_body')


class TipLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tip
        fields = ('likes',)


class AnswerLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('likes',)


class TipDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tip
        fields = ('dislikes',)


class AnswerDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('dislikes',)
