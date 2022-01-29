from rest_framework import serializers
from .models import CustomUser, AuthCodeAgronomist, AuthCodeFarmer, AuthCodePolicyMaker


# Serializers are used to bind routes together with data from the DB
# they also specify the (JSON) shape of the data provided to the callers
# DOC serializers: https://www.django-rest-framework.org/api-guide/serializers/

# auxiliary function to match the auth code with a specific user
def checkUserAuthCode(user_data, code_object):
    if user_data['first_name'] != str(code_object.first_name):
        raise serializers.ValidationError("Invalid authorization code")

    if user_data['last_name'] != str(code_object.last_name):
        raise serializers.ValidationError("Invalid authorization code")

    if not bool(code_object.isValid):
        raise serializers.ValidationError("Authorization code not valid")


# make authcode not valid, given the role and the validated data of an user
def disableAuthCode(data):
    if data['role'] == 'farmer':
        auth_code_object = AuthCodeFarmer.objects.get(pk=data['auth_code'])
        auth_code_object.isValid = False
        auth_code_object.save()

    elif data['role'] == 'policymaker':
        auth_code_object = AuthCodePolicyMaker.objects.get(pk=data['auth_code'])
        auth_code_object.isValid = False
        auth_code_object.save()


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'latitude', 'longitude', 'auth_code', 'password', 'role')
        # blur auth_code and password in the user post
        extra_kwargs = {'password': {'write_only': True}, 'auth_code': {'write_only': True}}

    def validate(self, data):
        """
        Function called to validate the data before create.
        """
        # set username, it is implemented for robustness, to allow the usage of user_name in the future
        data['user_name'] = data['email']

        # validate role string
        roles = ['farmer', 'agronomist', 'policymaker']
        if not data['role'] in roles:
            raise serializers.ValidationError("Invalid role")

        # validate authorization code
        if data['role'] == roles[0]:

            if float(data['latitude']) > float(90) or float(data['latitude']) < float(-90):
                raise serializers.ValidationError("Invalid latitude")

            if float(data['longitude']) > float(80) or float(data['longitude']) < float(-180):
                raise serializers.ValidationError("Invalid longitude")

            try:
                auth_code_object = AuthCodeFarmer.objects.get(pk=data['auth_code'])
                checkUserAuthCode(user_data=data, code_object=auth_code_object) # assign auth code area to farmer
                data['area'] = auth_code_object.area
                data['district'] = auth_code_object.area.district
            except AuthCodeFarmer.DoesNotExist:
                raise serializers.ValidationError("Invalid farmer authorization code")

        elif data['role'] == roles[1]:
            try:
                auth_code_object = AuthCodeAgronomist.objects.get(pk=data['auth_code'])
            except AuthCodeAgronomist.DoesNotExist:
                raise serializers.ValidationError("Invalid agronomist authorization code")
            raise serializers.ValidationError("Registration for agronomist will be ready soon...")

        else:
            try:
                auth_code_object = AuthCodePolicyMaker.objects.get(pk=data['auth_code'])
                checkUserAuthCode(user_data=data, code_object=auth_code_object)
                data['district'] = auth_code_object.district    # assign auth code district to policymaker
            except AuthCodePolicyMaker.DoesNotExist:
                raise serializers.ValidationError("Invalid policy maker authorization code")

        return data

    def create(self, validated_data):
        # dynamically create district/area field based on the user type
        geo_args = {}
        if validated_data['role'] == 'farmer':
            geo_args = {'area': validated_data['area'], 'district': validated_data['district']}
        elif validated_data['role'] == 'policymaker':
            geo_args = {'district': validated_data['district']}

        # create user object
        user = CustomUser(
            first_name=validated_data['first_name'],
            email=validated_data['email'],
            last_name=validated_data['last_name'],
            auth_code=validated_data['auth_code'],
            role=validated_data['role'],
            user_name=validated_data['user_name'],
            latitude=validated_data['latitude'],
            longitude=validated_data['longitude'],
            is_active=True,     # the user is activated immediately, change here if needed
            **geo_args
        )

        # save password hashed
        user.set_password(validated_data['password'])
        user.save()

        # disable authcode
        disableAuthCode(data=validated_data)
        print("@@ Serializer execution...")
        return user
