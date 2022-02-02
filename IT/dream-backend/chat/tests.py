from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from django.contrib.auth.models import Group
from chat.models import HrMessage, TipMessage
from chat.views import hr_message_list, tip_message_list, hr_message_add, tip_message_add
from forum.models import Category
from request.models import HelpRequest, TipRequest
from users.models import CustomUser


class MessagesTestes(APITestCase):
    def setUp(self):
        """
        Context:
            farmers: f1,f2,f3
            policymakers: p1
            HR: hr1
            TR: tr1
            HRMessage: m1,m2
            TRMessage: t1, t2
            Category: c1
        """
        self.factory = APIRequestFactory()  # used to perform CRUD operations
        self.group_farmer = Group(name='farmer-group')
        self.group_policymaker = Group(name='policymaker-group')
        self.group_farmer.save()
        self.group_policymaker.save()

        self.f1 = CustomUser.objects.create(
            email='a@a.it',
            user_name='a@a.it',
            first_name='a',
            last_name='a',
            auth_code='a',
            password='a',
            latitude=1,
            longitude=1
        )
        self.f1.groups.add(self.group_farmer)
        self.f1.save()

        self.f2 = CustomUser.objects.create(
            email='b@a.it',
            user_name='b@a.it',
            first_name='b',
            last_name='b',
            auth_code='b',
            password='b',
            latitude=1,
            longitude=1
        )
        self.f2.groups.add(self.group_farmer)
        self.f2.save()

        self.f3 = CustomUser.objects.create(
            email='r@a.it',
            user_name='r@a.it',
            first_name='r',
            last_name='b',
            auth_code='b',
            password='b',
            latitude=1,
            longitude=1
        )
        self.f3.groups.add(self.group_farmer)
        self.f3.save()

        self.p1 = CustomUser.objects.create(
            email='d@a.it',
            user_name='d@a.it',
            first_name='d',
            last_name='d',
            auth_code='d',
            password='d',
            latitude=1,
            longitude=1
        )
        self.p1.groups.add(self.group_policymaker)
        self.p1.save()

        self.hr1 = HelpRequest(
            title='t',
            author=self.f2,
            receiver=self.f1,
            status='accepted',
            content='a'
        )
        self.hr1.save()

        self.m1 = HrMessage(
            body='a',
            isFromSender=True,
            reference_hr=self.hr1
        )
        self.m1.save()
        self.m2 = HrMessage(
            body='a',
            isFromSender=False,
            reference_hr=self.hr1
        )
        self.m2.save()

        self.cat1 = Category(
            name='c1'
        )
        self.cat1.save()

        self.tr1 = TipRequest(
            proposed_title='t',
            author=self.p1,
            receiver=self.f3,
            status='accepted',
            proposed_tip='a',
            category=self.cat1
        )
        self.tr1.save()

        self.mr1 = TipMessage(
            body='a',
            isFromFarmer=True,
            reference_tip=self.tr1
        )
        self.mr1.save()
        self.mr2 = TipMessage(
            body='a',
            isFromFarmer=False,
            reference_tip=self.tr1
        )
        self.mr2.save()

    def test_hr_message_to_string(self):
        """
        Ensure HR message conversion to string:
        """
        m3 = HrMessage(
            body='111',
            isFromSender=False,
            reference_hr=self.hr1
        )
        self.assertEqual(str(m3), '111')

    def test_tr_message_to_string(self):
        """
            TR message conversion to string:
        """
        m4 = TipMessage(
            body='222',
            isFromFarmer=False,
            reference_tip=self.tr1
        )
        self.assertEqual(str(m4), '222')

    def test_load_hr(self):
        """
        Ensure only participants can load HR messages.
        """
        url = reverse('chat:hrmessageload')

        # try access as anonymous
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try access with unauthorized user policymaker
        request = self.factory.get(url)
        force_authenticate(request, user=self.p1)
        response = hr_message_list(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try farmer request without id of the hr
        request = self.factory.get(url)
        force_authenticate(request, user=self.f1)
        response = hr_message_list(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # try correct farmer requests (f1 and f2)
        request = self.factory.get(url + '/?id=1')
        force_authenticate(request, user=self.f1)
        response = hr_message_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request = self.factory.get(url + '/?id=1')
        self.assertEqual(len(response.data), 2)

        force_authenticate(request, user=self.f2)
        response = hr_message_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # try unauthorized farmer request (f3)
        request = self.factory.get(url + '/?id=1')
        force_authenticate(request, user=self.f3)
        response = hr_message_list(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # try get not existing message list
        request = self.factory.get(url + '/?id=2')
        force_authenticate(request, user=self.f1)
        response = hr_message_list(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_send_hr_messages(self):
        """
        Ensure only participants can send HR messages.
        """
        url = reverse('chat:hrmessagecreate')

        # try access as anonymous
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try bad formatted request
        request = self.factory.post(url)
        force_authenticate(request, user=self.f1)
        response = hr_message_add(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # try to send invalid reference hr
        data = {'reference_hr': 10, 'body': 'aa'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = hr_message_add(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # message from unauthorized user
        data = {'reference_hr': self.hr1.id, 'body': 'aa'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f3)
        response = hr_message_add(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # try to send message (f1 f2) and verify it's saved
        data = {'reference_hr': self.hr1.id, 'body': 'aa'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = hr_message_add(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request = self.factory.get(url + '/?id=1')
        force_authenticate(request, user=self.f1)
        response = hr_message_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # +1 message

        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f2)
        response = hr_message_add(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request = self.factory.get(url + '/?id=1')
        force_authenticate(request, user=self.f2)
        response = hr_message_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # +2 message

        # try to send message to a non accepted hr
        self.hr1.status = 'not accepted'
        self.hr1.save()
        data = {'reference_hr': self.hr1.id, 'body': 'aa'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = hr_message_add(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        request = self.factory.get(url + '/?id=1')
        force_authenticate(request, user=self.f1)
        response = hr_message_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # number of message as before

    def test_load_tr(self):
        """
        Ensure only participants can load TR messages.
        """
        url = reverse('chat:trmessageload')

        # try access as anonymous
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try farmer request without id of the hr
        request = self.factory.get(url)
        force_authenticate(request, user=self.f1)
        response = tip_message_list(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # try farmer request without id of the tr
        request = self.factory.get(url)
        force_authenticate(request, user=self.f3)
        response = tip_message_list(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # try correct requests (f3 and p1)
        request = self.factory.get(url + '/?id=1')
        force_authenticate(request, user=self.f3)
        response = tip_message_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        request = self.factory.get(url + '/?id=1')
        force_authenticate(request, user=self.p1)
        response = tip_message_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # try unauthorized farmer request (f1)
        request = self.factory.get(url + '/?id=1')
        force_authenticate(request, user=self.f1)
        response = tip_message_list(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # try get not existing message list (p1)
        request = self.factory.get(url + '/?id=2')
        force_authenticate(request, user=self.p1)
        response = tip_message_list(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_send_tip_messages(self):
        """
        Ensure only participants can send TR messages.
        """
        url = reverse('chat:trmessagecreate')

        # try access as anonymous
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try bad formatted request
        request = self.factory.post(url)
        force_authenticate(request, user=self.f3)
        response = tip_message_add(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # try to send invalid reference tip
        data = {'reference_tip': 10, 'body': 'aa'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f3)
        response = tip_message_add(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # message from unauthorized user
        data = {'reference_tip': self.tr1.id, 'body': 'aa'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_message_add(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # try to send message (p1 f3) and verify it's saved
        data = {'reference_tip': self.tr1.id, 'body': 'aa'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f3)
        response = tip_message_add(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request = self.factory.get(url + '/?id=1')
        force_authenticate(request, user=self.f3)
        response = tip_message_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # +1 message

        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.p1)
        response = tip_message_add(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request = self.factory.get(url + '/?id=1')
        force_authenticate(request, user=self.p1)
        response = tip_message_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # +2 message

        # try to send message to a declined tr chat
        self.tr1.status = 'declined'
        self.tr1.save()
        data = {'reference_tip': self.tr1.id, 'body': 'aa'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f3)
        response = tip_message_add(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        request = self.factory.get(url + '/?id=1')
        force_authenticate(request, user=self.f3)
        response = tip_message_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # number of message as before
