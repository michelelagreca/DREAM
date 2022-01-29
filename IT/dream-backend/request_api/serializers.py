from rest_framework import serializers
from request.models import HelpRequest, TipRequest


# Serializers are used to bind routes together with data from the DB
# they also specify the (JSON) shape of the data provided at the callers
# DOC serializers: https://www.django-rest-framework.org/api-guide/serializers/

class HRSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpRequest
        fields = ('id', 'title', 'author', 'content', 'status')

class TRSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipRequest
        fields = ('id', 'proposed_title', 'author', 'proposed_tip', 'status')
