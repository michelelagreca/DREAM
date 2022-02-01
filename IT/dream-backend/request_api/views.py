import math
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from forum.models import Tip
from request.models import HelpRequest, HR_OPTIONS_EXT, TipRequest, TR_OPTIONS_EXT
from users.models import CustomUser
from .serializers import HRSerializer, HRChangeStatusSerializer, TRSerializer, TRChangeStatusSerializer
from django.db.models import Q


# import here all the needed DB models
# from forum.models import MODEL_NAME

# import serializers fro each model, they are needed to create the endpoints
# from .serializers import SERIALIZER_NAME


# --------------  HELP REQUEST  --------------


@api_view(['POST'])
def send_hr_farmer(request):
    if not request.user.groups.filter(name = "farmer-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
    incoming_hr = HRSerializer(data=request.data)

    print(f'@ {request.data}')
    print(f'@ {incoming_hr.is_valid()}')
    if not incoming_hr.is_valid():
        return Response(data="Invalid Request", status=status.HTTP_400_BAD_REQUEST)

    if not request.user.role == 'farmer':
        return Response(status=status.HTTP_401_UNAUTHORIZED)

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
    if not request.user.groups.filter(name = "farmer-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
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
    if not request.user.groups.filter(name = "farmer-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
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


# --------------  TIP REQUEST  --------------

@api_view(['POST'])
def send_tip_request(request):
    if not request.user.groups.filter(name = "policymaker-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
    incoming_tr = TRSerializer(data=request.data)

    # print(f'@ {request.data}')
    # print(f'@ {incoming_hr.is_valid()}')

    if not incoming_tr.is_valid():
        return Response(data="Invalid Request", status=status.HTTP_400_BAD_REQUEST)

    if not request.user.role == 'policymaker':
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    # try to get farmer associated to the request
    try:
        farmer = CustomUser.objects.get(role=incoming_tr.validated_data['receiver'])
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # farmer belong to a district where the policy maker is not in charge
    if farmer.zone.district != request.user.district:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    # creation and save
    new_request = TipRequest(
        proposed_title=incoming_tr.validated_data['proposed_title'],
        proposed_tip=incoming_tr.validated_data['proposed_tip'],
        category=incoming_tr.validated_data['category'],
        author=request.user,
        receiver=farmer,
        status='pending'
    )
    new_request.save()

    return Response(data="TR successfully sent", status=status.HTTP_200_OK)


@api_view(['POST'])
def change_status_tip_request(request):
    if not request.user.groups.filter(name = "policymaker-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
    # pass http request data to custom serializer
    tr_serializer = TRChangeStatusSerializer(data=request.data)
    print(request.data)
    print(tr_serializer.is_valid())
    # check validation
    if not tr_serializer.is_valid():
        return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)

    # read validated data
    tr_id = tr_serializer.validated_data["tr_id"]
    tr_status = tr_serializer.validated_data["status"]
    tr_proposed_title = tr_serializer.validated_data["proposed_title"]
    tr_proposed_tip = tr_serializer.validated_data["proposed_tip"]

    print(f'new : ${tr_serializer.validated_data}')

    # check option validity
    if tr_status not in TR_OPTIONS_EXT:
        return Response("Invalid Option", status=status.HTTP_400_BAD_REQUEST)

    # get associated tip request
    try:
        tr = TipRequest.objects.get(pk=tr_id)
    except TipRequest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    print(f'old: ${tr.status} ')

    if request.user != tr.author and request.user != tr.receiver:
        return Response(data="You cannot modify this tr", status=status.HTTP_401_UNAUTHORIZED)

    # intercept the policymaker request for modification tr.status is the old status
    if request.user == tr.author and tr.status == 'review' and tr_status == 'farmer':
        tr.proposed_title = tr_proposed_title
        tr.proposed_tip = tr_proposed_tip

    # intercept the farmer request to review
    if request.user == tr.receiver and tr.status == 'farmer' and tr_status == 'review':
        tr.proposed_title = tr_proposed_title
        tr.proposed_tip = tr_proposed_tip

    tr.status = tr_status
    tr.save()

    # intercept changing od status from review to accepted made by policymakers
    if request.user == tr.author and tr.status == 'review' and tr.status == 'accepted':
        tip = Tip(
            title=tr.proposed_title,
            text_body=tr.proposed_tip,
            author=tr.receiver,
            category=tr.category,
            area=tr.receiver.area,
            is_star=False,
        )
        tip.save()

    return Response(data="TR status updated", status=status.HTTP_200_OK)


@api_view(['GET'])
def tr_list_farmer(request):
    if not request.user.groups.filter(name = "farmer-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
    # filter hr by user
    qs_dict = TipRequest.objects.filter(receiver=request.user).values()  # get queryset in dictionary form

    # add extra field to determine if the user is the sender or receiver of the hr
    if request.user.role != 'farmer':
        Response(status=status.HTTP_401_UNAUTHORIZED)

    return Response(data=qs_dict, status=status.HTTP_200_OK, content_type='application/json')


@api_view(['GET'])
def tr_list_policymaker(request):
    if not request.user.groups.filter(name = "policymaker-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
    # filter hr by user
    qs_dict = TipRequest.objects.filter(author=request.user).values()  # get queryset in dictionary form

    # add extra field to determine if the user is the sender or receiver of the hr
    if request.user.role != 'policymaker':
        Response(status=status.HTTP_401_UNAUTHORIZED)

    return Response(data=qs_dict, status=status.HTTP_200_OK, content_type='application/json')


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
