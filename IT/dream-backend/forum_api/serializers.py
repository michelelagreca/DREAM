from rest_framework import serializers
from forum.models import Question


# Serializers are used to bind routes together with data from the DB
# they also specify the (JSON) shape of the data provided to the callers
# DOC serializers: https://www.django-rest-framework.org/api-guide/serializers/


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'title', 'author', 'excerpt', 'content', 'status')

