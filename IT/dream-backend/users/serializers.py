from rest_framework import serializers
from .models import CustomUser, AuthCodeAgronomist, AuthCodeFarmer, AuthCodePolicyMaker


# Serializers are used to bind routes together with data from the DB
# they also specify the (JSON) shape of the data provided to the callers
# DOC serializers: https://www.django-rest-framework.org/api-guide/serializers/


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'auth_code', 'password', 'role')
        # blur auth_code and password in the user post
        extra_kwargs = {'password': {'write_only': True}, 'auth_code': {'write_only': True}}

    def validate(self, data):
        """
        Function called to validate the data before create.
        DOC: https://www.django-rest-framework.org/api-guide/serializers/#validation
        """
        # validate role string
        roles = ['farmer', 'policymaker', 'agronomist']
        if not data['role'] in roles:
            raise serializers.ValidationError("Invalid role")

        # if data['role'] == roles[0]:
        print(data)

        try:
            auth_code = AuthCodeFarmer.objects.get(pk=data['auth_code'])
            print(auth_code)
        except AuthCodeFarmer.DoesNotExist:
            raise serializers.ValidationError("Invalid authorization code")

        return data

    def create(self, validated_data):
        # validate user data
        user = CustomUser(
            first_name=validated_data['first_name'],
            email=validated_data['email'],
            last_name=validated_data['last_name'],
            auth_code=validated_data['auth_code'],
            role=validated_data['role'],
        )
        # password saved hashed
        user.set_password(validated_data['password'])
        user.save()
        return user
