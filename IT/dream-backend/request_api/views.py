import math

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.decorators import api_view
from request.models import HelpRequest, HR_OPTIONS_EXT
from users.models import CustomUser
from .serializers import HRSerializer, HRChangeStatusSerializer
from django.db.models import Q


# import here all the needed DB models
# from forum.models import MODEL_NAME

# import serializers fro each model, they are needed to create the endpoints
# from .serializers import SERIALIZER_NAME

@api_view(['POST'])
def send_hr_farmer(request):
    incoming_hr = HRSerializer(data=request.data)

    print(f'@ {request.data}')
    print(f'@ {incoming_hr.is_valid()}')
    if not incoming_hr.is_valid():
        return Response(data="Invalid Request", status=status.HTTP_400_BAD_REQUEST)

    """
    if not request.user == 'farmer':
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    """
    sender_lat = request.user.latitude
    sender_long = request.user.longitude

    farmer_qs = CustomUser.objects.filter(role='farmer')
    hr_receivers = []

    # build the list of nearby farmer that will be the receivers
    for farmer in farmer_qs:
        if not farmer == request.user:
            lat = farmer.latitude
            lon = farmer.longitude
            x_distance = abs(sender_lat - lat)
            y_distance = abs(sender_long - lon)
            # conversion in km
            x_km = 111.0 * float(x_distance)
            y_km = 111.33 * float(y_distance)
            # radius in km
            radius = 10.0
            # verify proximity condition
            if math.sqrt(x_km ** 2 + y_km ** 2) <= radius:
                hr_receivers.append(farmer)

    # case of empty list
    if len(hr_receivers) <= 0:
        return Response(data="No farmer nearby", status=status.HTTP_204_NO_CONTENT)

    # TODO manage timestamp
    for receiver_user in hr_receivers:
        new_request = HelpRequest(
            title=incoming_hr.validated_data['title'],
            # timestamp=incoming_hr.validated_data['timestamp'],
            content=incoming_hr.validated_data['content'],
            # slug=incoming_hr.validated_data['slug'],
            # published=incoming_hr.validated_data['published'],
            author=request.user,
            receiver=receiver_user,
            status='not_accepted'
        )
        new_request.save()

    farmer_number = len(hr_receivers)
    return Response(data="HR successfully sent to " + str(farmer_number), status=status.HTTP_200_OK)


@api_view(['POST'])
def change_status_hr_farmer(request):
    # pass http request data to custom serializer
    hr_serializer = HRChangeStatusSerializer(data=request.data)

    # check validation
    if not hr_serializer.is_valid():
        return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)

    # read validated data
    hr_id = hr_serializer.validated_data["hr_id"]
    hr_status = hr_serializer.validated_data["status"]

    if hr_status not in HR_OPTIONS_EXT:
        return Response("Invalid Option", status=status.HTTP_400_BAD_REQUEST)

    try:
        hr = HelpRequest.objects.get(pk=hr_id)
    except HelpRequest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user != hr.author and request.user != hr.receiver:
        return Response(data="You cannot modify this hr", status=status.HTTP_401_UNAUTHORIZED)

    hr.status = hr_status
    hr.save()

    return Response(data="HR status updated", status=status.HTTP_200_OK)


@api_view(['GET'])
def hr_list_farmer(request):
    # filter hr by user
    qs_dict = HelpRequest.objects.filter(
        Q(author=request.user) | Q(receiver=request.user)).values()  # get queryset in dictionary form

    # add extra field to determine if the user is the sender or receiver of the hr
    for hr in qs_dict:
        if hr['author_id'] == request.user.id:
            hr['is_sender'] = True
        else:
            hr['is_sender'] = False

    return Response(data=qs_dict, status=status.HTTP_200_OK, content_type='application/json')


# ADD HERE GENERIC VIEW FOR DEBUGGING PORPOUSE, THEY ARE INCLUDED IN THE REST FRAMEWORK
class RequestList(generics.ListCreateAPIView):
    # queryset = HelpRequest.hrobjects.all()
    # serializer_class = HRSerializer
    pass


class RequestDetail(generics.RetrieveUpdateDestroyAPIView):
    # queryset = HelpRequest.objects.all()
    # serializer_class = HRSerializer
    pass


""" Concrete View Classes
#CreateAPIView
Used for create-only endpoints.
#ListAPIView
Used for read-only endpoints to represent a collection of model instances.
#RetrieveAPIView
Used for read-only endpoints to represent a single model instance.
#DestroyAPIView
Used for delete-only endpoints for a single model instance.
#UpdateAPIView
Used for update-only endpoints for a single model instance.
##ListCreateAPIView
Used for read-write endpoints to represent a collection of model instances.
RetrieveUpdateAPIView
Used for read or update endpoints to represent a single model instance.
#RetrieveDestroyAPIView
Used for read or delete endpoints to represent a single model instance.
#RetrieveUpdateDestroyAPIView
Used for read-write-delete endpoints to represent a single model instance.
"""
