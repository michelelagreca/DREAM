from .serializers import RegistrationSerializer
from rest_framework import generics


# Create your views here.
class PostUser(generics.CreateAPIView):
    # queryset = Question.objects.all()
    serializer_class = RegistrationSerializer
