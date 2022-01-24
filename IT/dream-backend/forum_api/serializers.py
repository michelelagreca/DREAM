from rest_framework import serializers
from forum.models import Question, Category, Tip


# Serializers are used to bind routes together with data from the DB
# they also specify the (JSON) shape of the data provided to the callers
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

class TipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tip
        fields = ('id', 'timestamp', 'title', 'text_body', 'author', 'category', 'area', 'likes', 'dislikes', 'is_star')

# class TipLikesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tip
#         fields = ('likes',)

#     def update(self, instance, validated_data): 
#         instance.likes = validated_data.get('likes', instance.likes)
#         instance.save()
#         return instance

# class TipDislikesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tip
#         fields = ('dislikes',)