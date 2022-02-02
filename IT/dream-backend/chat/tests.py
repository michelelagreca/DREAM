from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase, APIRequestFactory, force_authenticate
from django.contrib.auth.models import Group

from chat.models import HrMessage, TipMessage
from chat.views import hr_message_list, tip_message_list
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
