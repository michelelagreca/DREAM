from rest_framework.decorators import api_view

from .models import CustomUser
from .serializers import RegistrationSerializer
from rest_framework import generics
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class PostUser(generics.CreateAPIView):
    # queryset = Question.objects.all()
    serializer_class = RegistrationSerializer


# customization of the token jwt response
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        # standard response
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # extra responses
        data['role'] = self.user.role

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class BlacklistTokenUpdateView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_info(request):
    if request.user.is_anonymous:
        return Response(data=[], status=status.HTTP_200_OK)

    user_dict = CustomUser.objects.filter(pk=request.user.id) \
        .values('first_name', 'last_name', 'role', 'email', 'area_id', 'district_id')

    return Response(data=user_dict, status=status.HTTP_200_OK, content_type='application/json')
