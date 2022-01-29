from rest_framework import serializers


# here are defined some general serializers


class IdGeneralSerializer(serializers.Serializer):
    id = serializers.IntegerField()
