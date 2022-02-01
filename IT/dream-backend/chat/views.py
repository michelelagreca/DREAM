from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status

from chat.models import HrMessage, TipMessage
from chat.serializers import HrMessageSerializer, TipMessageSerializer
from core.serializers import IdGeneralSerializer
from request.models import HelpRequest, TipRequest


# --------------  HELP REQUEST  --------------

@api_view(['GET'])
def hr_message_list(request):
    if not request.user.groups.filter(name = "farmer-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
    hr_serializer = IdGeneralSerializer(data=request.GET)

    # check validation
    if not hr_serializer.is_valid():
        return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)

    # read validated data
    hr_id = hr_serializer.validated_data["id"]

    # try to get reference hr
    try:
        hr = HelpRequest.objects.get(pk=hr_id)
    except HelpRequest.DoesNotExist:
        return Response(data="HR not found", status=status.HTTP_404_NOT_FOUND)

    # check if either the user is the author or the receiver
    if hr.author != request.user and hr.receiver != request.user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    # create message response object
    messages_dict = HrMessage.objects.filter(reference_hr=hr).values()

    return Response(data=messages_dict, status=status.HTTP_200_OK, content_type='application/json')


@api_view(['POST'])
def hr_message_add(request):
    if not request.user.groups.filter(name = "farmer-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
    message_serializer = HrMessageSerializer(data=request.data)

    # check validation
    if not message_serializer.is_valid():
        return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)

    # read validated data
    hr_ref = message_serializer.validated_data["reference_hr"]

    # check if either the user is the author or the receiver
    is_from_sender = False
    if hr_ref.author == request.user:
        is_from_sender = True
    elif hr_ref.author != request.user and hr_ref.receiver != request.user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    message = HrMessage(
        body=message_serializer.validated_data['body'],
        reference_hr=hr_ref,
        isFromSender=is_from_sender
    )

    message.save()
    return Response(data="Message sent", status=status.HTTP_200_OK, content_type='application/json')


# --------------  TIP REQUEST  --------------

@api_view(['GET'])
def tip_message_list(request):
    if not request.user.groups.filter(name = "farmer-group").exists() and not request.user.groups.filter(name = "policymaker-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
    tip_serializer = IdGeneralSerializer(data=request.GET)

    # check validation
    if not tip_serializer.is_valid():
        return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)

    # read validated data
    tip_id = tip_serializer.validated_data["id"]

    # try to get reference hr
    try:
        tip = TipRequest.objects.get(pk=tip_id)
    except HelpRequest.DoesNotExist:
        return Response(data="Tip not found", status=status.HTTP_404_NOT_FOUND)

    # check if either the user is the author or the receiver
    if tip.author != request.user and tip.receiver != request.user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    # create message response object
    messages_dict = TipMessage.objects.filter(reference_tip=tip).values()

    return Response(data=messages_dict, status=status.HTTP_200_OK, content_type='application/json')


@api_view(['POST'])
def tip_message_add(request):
    if not request.user.groups.filter(name = "farmer-group").exists() and not request.user.groups.filter(name = "policymaker-group").exists():
        return Response(data="User not allowed", status=status.HTTP_403_FORBIDDEN)
    message_serializer = TipMessageSerializer(data=request.data)

    # check validation
    if not message_serializer.is_valid():
        return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)

    # read validated data
    tip_ref = message_serializer.validated_data["reference_tip"]

    # check if either the user is the author or the receiver
    is_from_farmer = False
    if tip_ref.author == request.user:
        is_from_farmer = True
    elif tip_ref.author != request.user and tip_ref.receiver != request.user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    message = TipMessage(
        body=message_serializer.validated_data['body'],
        reference_tip=tip_ref,
        isFromFarmer=is_from_farmer
    )

    message.save()
    return Response(data="Message sent", status=status.HTTP_200_OK, content_type='application/json')
