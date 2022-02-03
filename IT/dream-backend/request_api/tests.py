from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase, APIRequestFactory, force_authenticate
from django.contrib.auth.models import Group
from chat.models import HrMessage, TipMessage
from chat.views import hr_message_list, tip_message_list, hr_message_add, tip_message_add
from forum.models import Category, Tip
from request.models import HelpRequest, TipRequest
from request_api.views import send_hr_farmer, send_tip_request, hr_list_farmer, change_status_hr_farmer, tr_list_farmer, \
    tr_list_policymaker, change_status_tip_request
from users.models import CustomUser, District, Area


class RequestTestes(APITestCase):

    def setUp(self):
        """
        Context:
            farmers: f1,f2,f3
            policymakers: p1,p2
            HR: hr1; f1->f2
            TR: tr1; p1->f3
            Category: c1
            area: a1,a2
            district d1,d2
        """
        self.factory = APIRequestFactory()  # used to perform CRUD operations
        self.group_farmer = Group(name='farmer-group')
        self.group_policymaker = Group(name='policymaker-group')
        self.group_farmer.save()
        self.group_policymaker.save()

        self.dis1 = District(
            name='d1'
        )
        self.dis2 = District(
            name='d2'
        )
        self.dis1.save()
        self.dis2.save()

        self.ar1 = Area(
            name='a1',
            district=self.dis1
        )
        self.ar2 = Area(
            name='a2',
            district=self.dis2
        )
        self.ar1.save()
        self.ar2.save()

        self.f1 = CustomUser.objects.create(
            email='a@a.it',
            user_name='a@a.it',
            first_name='a',
            last_name='a',
            auth_code='a',
            password='a',
            latitude=1,
            longitude=1,
            area=self.ar1
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
            longitude=1,
            area=self.ar2
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
            longitude=1,
            district=self.dis1,
        )
        self.p1.groups.add(self.group_policymaker)
        self.p1.save()

        self.p2 = CustomUser.objects.create(
            email='p2@a.it',
            user_name='p2@a.it',
            first_name='p2',
            last_name='p2',
            auth_code='p2',
            password='p2',
            latitude=1,
            longitude=1
        )
        self.p2.groups.add(self.group_policymaker)
        self.p2.save()

        self.hr1 = HelpRequest(
            title='t',
            author=self.f2,
            receiver=self.f1,
            status='not_accepted',
            content='a'
        )
        self.hr1.save()

        self.cat1 = Category(
            name='c1'
        )
        self.cat1.save()

        self.tr1 = TipRequest(
            proposed_title='t',
            author=self.p1,
            receiver=self.f3,
            status='pending',
            proposed_tip='a',
            category=self.cat1
        )
        self.tr1.save()

    def test_send_hr_farmer(self):
        """
            Check correctness of send HR mechanism.
        """
        url = reverse('request_api:send_hr_farmer')

        # try access as anonymous
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try access with unauthorized user group
        request = self.factory.post(url)
        force_authenticate(request, user=self.p1)
        response = send_hr_farmer(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try farmer request with invalid data
        data = {'reference_hr': 10, 'body': 'aa'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = send_hr_farmer(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # test distance with 9.99km distance and 10.01 km distance

        x_base = self.f1.latitude
        y_base = self.f1.longitude

        x_shift_legal = 9.99 / 111.0
        x_shift_illegal = 10.01 / 111.0

        y_shift_legal = 9.99 / 111.33
        y_shift_illegal = 10.01 / 111.33

        self.fill1 = CustomUser.objects.create(
            email='fill1@a.it',
            user_name='fill1@a.it',
            first_name='fill1',
            last_name='fill1',
            auth_code='a',
            password='a',
            latitude=x_base + x_shift_illegal,
            longitude=y_base,
            area=self.ar1,
            role="farmer"
        )
        self.fill2 = CustomUser.objects.create(
            email='fill2@a.it',
            user_name='fill2@a.it',
            first_name='fill2',
            last_name='fill2',
            auth_code='a',
            password='a',
            latitude=x_base,
            longitude=y_base + y_shift_illegal,
            area=self.ar1,
            role="farmer"
        )
        self.fill1.groups.add(self.group_farmer)
        self.fill1.save()
        self.fill2.groups.add(self.group_farmer)
        self.fill2.save()

        data = {'title': 'title', 'content': 'hr1'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = send_hr_farmer(request)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        request = self.factory.get(url)
        force_authenticate(request, user=self.f1)
        response = hr_list_farmer(request)
        self.assertEqual(len(response.data), 1)  # 1 default + 0 just sent

        self.fl1 = CustomUser.objects.create(
            email='fl1@a.it',
            user_name='fl1@a.it',
            first_name='fl1',
            last_name='fl1',
            auth_code='a',
            password='a',
            latitude=x_base + x_shift_legal,
            longitude=y_base,
            area=self.ar1,
            role="farmer"
        )
        self.fl2 = CustomUser.objects.create(
            email='fl2@a.it',
            user_name='fl2@a.it',
            first_name='fl2',
            last_name='fl2',
            auth_code='a',
            password='a',
            latitude=x_base,
            longitude=y_base + y_shift_legal,
            area=self.ar1,
            role="farmer"
        )
        self.fl1.groups.add(self.group_farmer)
        self.fl1.save()
        self.fl2.groups.add(self.group_farmer)
        self.fl2.save()

        data = {'title': 'title', 'content': 'hr1'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = send_hr_farmer(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        request = self.factory.get(url)  # sender get
        force_authenticate(request, user=self.f1)
        response = hr_list_farmer(request)
        self.assertEqual(len(response.data), 3)  # 1 default + 2 just sent

        request = self.factory.get(url)  # legal sender get
        force_authenticate(request, user=self.fl1)
        response = hr_list_farmer(request)
        self.assertEqual(len(response.data), 1)  # 1 hr just received
        request = self.factory.get(url)
        force_authenticate(request, user=self.fl2)
        response = hr_list_farmer(request)
        self.assertEqual(len(response.data), 1)  # 1 hr just received
        request = self.factory.get(url)

        force_authenticate(request, user=self.fill1)  # illegal sender get
        response = hr_list_farmer(request)
        self.assertEqual(len(response.data), 0)  # 0 hr just received
        request = self.factory.get(url)
        force_authenticate(request, user=self.fill2)
        response = hr_list_farmer(request)
        self.assertEqual(len(response.data), 0)  # 0 hr just received

    def test_read_hr_farmer(self):
        """
           Check correctness of reading HR for sender and receiver.
        """
        url = reverse('request_api:read_hr_farmer')

        # try access as anonymous
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try access with unauthorized user group
        request = self.factory.get(url)
        force_authenticate(request, user=self.p1)
        response = hr_list_farmer(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # access of list hr of farmer
        request = self.factory.get(url)  # legal sender get
        force_authenticate(request, user=self.f1)
        response = hr_list_farmer(request)
        self.assertEqual(len(response.data), 1)  # 1 default
        request = self.factory.get(url)
        force_authenticate(request, user=self.f3)
        response = hr_list_farmer(request)
        self.assertEqual(len(response.data), 0)  # 0 hr default
        request = self.factory.get(url)

    def test_status_hr_farmer(self):
        """
            Check correctness of send HR mechanism.
        """
        url = reverse('request_api:change_status_hr_farmer')

        # try access as anonymous
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try access with unauthorized user group
        request = self.factory.post(url)
        force_authenticate(request, user=self.p1)
        response = change_status_hr_farmer(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try farmer request with invalid data
        data = {'hr_id': 1}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = change_status_hr_farmer(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'hr_id': 2, 'status': 'accepted'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = change_status_hr_farmer(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # test unauthorized farmer
        data = {'hr_id': 1, 'status': 'accepted'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f3)
        response = change_status_hr_farmer(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # test forbidden  sender auto accept
        data = {'hr_id': 1, 'status': 'accepted'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f2)
        response = change_status_hr_farmer(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # test receiver accept
        data = {'hr_id': 1, 'status': 'accepted'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = change_status_hr_farmer(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test invalid option
        data = {'hr_id': 1, 'status': 'corrupted'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = change_status_hr_farmer(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # test forbidden decline after accepted state
        data = {'hr_id': 1, 'status': 'declined'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = change_status_hr_farmer(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # test valid close state
        data = {'hr_id': 1, 'status': 'closed'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = change_status_hr_farmer(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # prevent any change after close state
        data = {'hr_id': 1, 'status': 'accepted'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = change_status_hr_farmer(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_send_tr_policymaker(self):
        """
           Check correctness of send TR mechanism.
        """
        url = reverse('request_api:send_tip_request')

        # try access as anonymous
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try access with unauthorized user group
        request = self.factory.post(url)
        force_authenticate(request, user=self.f1)
        response = send_tip_request(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try request with invalid data
        data = {'reference_tip': 10}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.p1)
        response = send_tip_request(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # try policy maker not in the district of the farmer
        data = {'proposed_title': 't', 'proposed_tip': 't1', 'receiver': 3, 'category': 'c1'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.p1)
        response = send_tip_request(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # try valid request
        data = {'proposed_title': 't', 'proposed_tip': 't1', 'receiver': 1, 'category': 'c1'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.p1)
        response = send_tip_request(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_tr_farmer(self):
        """
           Check correctness of reading TR for receiver (farmer).
        """
        url = reverse('request_api:read_tr_farmer')

        # try access as anonymous
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try access with unauthorized user group
        request = self.factory.get(url)
        force_authenticate(request, user=self.p1)
        response = tr_list_farmer(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # access tr list of farmer
        request = self.factory.get(url)  # legal sender get
        force_authenticate(request, user=self.f1)
        response = tr_list_farmer(request)
        self.assertEqual(len(response.data), 0)  # 0 tr default
        request = self.factory.get(url)
        force_authenticate(request, user=self.f3)
        response = tr_list_farmer(request)
        self.assertEqual(len(response.data), 1)  # 1 tr default
        request = self.factory.get(url)

    def test_read_tr_policymaker(self):
        """
           Check correctness of reading TR for sender (policymaker).
        """
        url = reverse('request_api:read_tr_policymaker')

        # try access as anonymous
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try access with unauthorized user group
        request = self.factory.get(url)
        force_authenticate(request, user=self.f1)
        response = tr_list_policymaker(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # access tr list of policymakers
        request = self.factory.get(url)  # legal sender get
        force_authenticate(request, user=self.p1)
        response = tr_list_policymaker(request)
        self.assertEqual(len(response.data), 1)  # 1 tr default
        request = self.factory.get(url)
        force_authenticate(request, user=self.p2)
        response = tr_list_policymaker(request)
        self.assertEqual(len(response.data), 0)  # 0 tr default

    def test_status_tr(self):
        """
            Check correctness of tip request change status mechanism
        """
        url = reverse('request_api:change_status_tip_request')
        url_get_tip = reverse('forum_api:tiplistcreate')

        # try access as anonymous
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try farmer request with invalid data
        data = {'tr_id': 1, 'status': 'accepted', 'proposed_title': 'aa'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f3)
        response = change_status_tip_request(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # test invalid option
        data = {'tr_id': 1, 'status': 'corrupted', 'proposed_title': 'aa', 'proposed_tip': 'aa'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f3)
        response = change_status_tip_request(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # test not existent tr
        data = {'tr_id': 2, 'status': 'accepted', 'proposed_title': 'aa', 'proposed_tip': 'aa'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f3)
        response = change_status_tip_request(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # test forbidden auto accept policymaker
        data = {'tr_id': 1, 'status': 'accepted', 'proposed_title': 'aa', 'proposed_tip': 'aa'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.p1)
        response = change_status_tip_request(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # test unauthorized farmer
        data = {'tr_id': 1, 'status': 'accepted', 'proposed_title': 'aa', 'proposed_tip': 'aa'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = change_status_tip_request(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # test forbidden accept farmer
        data = {'tr_id': 1, 'status': 'accepted', 'proposed_title': 'aa', 'proposed_tip': 'aa'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f3)
        response = change_status_tip_request(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # test quick decline policymaker
        data = {'tr_id': 1, 'status': 'declined', 'proposed_title': 'aa', 'proposed_tip': 'aa'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.p1)
        response = change_status_tip_request(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test declined farmer
        self.tr1.status = 'pending'
        self.tr1.save()
        data = {'tr_id': 1, 'status': 'declined', 'proposed_title': 'aa', 'proposed_tip': 'aa'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f3)
        response = change_status_tip_request(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test start modification farmer
        self.tr1.status = 'pending'
        self.tr1.save()
        data = {'tr_id': 1, 'status': 'farmer', 'proposed_title': 'aa', 'proposed_tip': 'aa'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f3)
        response = change_status_tip_request(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test forbidden farmer change while reviewing
        self.tr1.status = 'review'
        self.tr1.save()
        data = {'tr_id': 1, 'status': 'farmer', 'proposed_title': 'aa', 'proposed_tip': 'aa'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f3)
        response = change_status_tip_request(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # test forbidden policymaker change while farmer turn
        self.tr1.status = 'farmer'
        self.tr1.save()
        data = {'tr_id': 1, 'status': 'review', 'proposed_title': 'aa', 'proposed_tip': 'aa'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.p1)
        response = change_status_tip_request(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # test tip request creation after acceptance
        response = self.client.get(url_get_tip, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        self.tr1.status = 'review'
        self.tr1.save()
        data = {'tr_id': 1, 'status': 'accepted', 'proposed_title': 'test_title', 'proposed_tip': 'test_tip'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.p1)
        response = change_status_tip_request(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url_get_tip, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # test modification of an accepted tr
        self.tr1.status = 'accepted'
        self.tr1.save()
        data = {'tr_id': 1, 'status': 'review', 'proposed_title': 'aa', 'proposed_tip': 'aa'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.p1)
        response = change_status_tip_request(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # test update of tip by farmer + counter update of policymaker
        self.tr1.status = 'farmer'
        self.tr1.save()
        new_title = 'new title'
        new_tip = 'new tip'
        data = {'tr_id': 1, 'status': 'review', 'proposed_title': new_title, 'proposed_tip': new_tip}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f3)
        response = change_status_tip_request(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TipRequest.objects.get(pk=self.tr1.id).proposed_title, new_title)
        self.assertEqual(TipRequest.objects.get(pk=self.tr1.id).proposed_tip, new_tip)

        new_title = 'new title policy'
        new_tip = 'new tip policy'
        data = {'tr_id': 1, 'status': 'farmer', 'proposed_title': new_title, 'proposed_tip': new_tip}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.p1)
        response = change_status_tip_request(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TipRequest.objects.get(pk=self.tr1.id).proposed_title, new_title)
        self.assertEqual(TipRequest.objects.get(pk=self.tr1.id).proposed_tip, new_tip)
