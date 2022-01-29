from rest_framework import serializers
from chat.models import HrMessage


class HrMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HrMessage
        fields = ('id', 'body', 'reference_hr')


class TipMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HrMessage
        fields = ('id', 'body', 'reference_tip')
