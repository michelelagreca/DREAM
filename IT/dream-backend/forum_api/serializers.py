from rest_framework import serializers
from forum.models import Question, Category


# Serializers are used to bind routes together with data from the DB
# they also specify the (JSON) shape of the data provided at the callers
# DOC serializers: https://www.django-rest-framework.org/api-guide/serializers/


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)
    

class QuestionSerializer(serializers.ModelSerializer):
    
    #category = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ('id', 'timestamp', 'title', 'text_body', 'author', 'category', 'area')

    # def get_category(self, category):
    #       return category.category.name 
    # this was to show the name of the category in the json, instead of the number referring the id