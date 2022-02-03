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
from users.models import CustomUser, District, Area, AuthCodeFarmer, AuthCodePolicyMaker, AuthCodeAgronomist
from users.views import PostUser, user_info, MyTokenObtainPairSerializer, MyTokenObtainPairView
from rest_framework.test import APIClient
from django.contrib.auth.models import Group


class UserTestes(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()  # used to perform CRUD operations
        self.group_farmer = Group(name='farmer-group')
        self.group_policymaker = Group(name='policymaker-group')
        self.client = APIClient()

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
            email='test@a.it',
            user_name='test@a.it',
            first_name='fname',
            last_name='lname',
            auth_code='aa',
            password='a',
            latitude=10,
            longitude=10,
            area=self.ar1,
            role='farmer'
        )
        self.f1.groups.add(self.group_farmer)
        self.f1.save()

        self.p1 = CustomUser.objects.create(
            email='ptest@a.it',
            user_name='pa@a.it',
            first_name='pfname',
            last_name='plname',
            auth_code='paa',
            password='pa',
            latitude=10,
            longitude=10,
            district=self.dis1,
            role='policymaker'
        )
        self.p1.groups.add(self.group_policymaker)
        self.p1.save()

        self.aF1 = AuthCodeFarmer(
            code='AA',
            first_name='f1',
            last_name='f1',
            area=self.ar1,
            isValid=True,
        )
        self.aF1.save()
        self.aF2 = AuthCodeFarmer(
            code='BB',
            first_name='f1',
            last_name='f1',
            area=self.ar1,
            isValid=False,
        )
        self.aF2.save()

        self.aP1 = AuthCodePolicyMaker(
            code='PP',
            first_name='f1',
            last_name='f1',
            district=self.dis1,
            isValid=True,
        )
        self.aP1.save()
        self.aP2 = AuthCodePolicyMaker(
            code='BB',
            first_name='f1',
            last_name='f1',
            district=self.dis1,
            isValid=False,
        )
        self.aP2.save()
        self.aAG1 = AuthCodeAgronomist(
            code='GG',
            first_name='f1',
            last_name='f1',
            area=self.ar1,
            isValid=False,
        )
        self.aAG1.save()

    def test_farmer_signup(self):
        url = reverse('users:user_create')

        # try farmer request with invalid first name and last name
        data = {'email': 'aa@a.it', 'first_name': 'f11', 'last_name': 'f1', 'latitude': '0', 'longitude': '0',
                'auth_code': 'AA', 'password': 'a', 'role': 'farmer'}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'email': 'aa@a.it', 'first_name': 'f1', 'last_name': 'f11', 'latitude': '0', 'longitude': '0',
                'auth_code': 'AA', 'password': 'a', 'role': 'farmer'}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # try farmer request with invalid latitude longitude
        data = {'email': 'aa@a.it', 'first_name': 'f1', 'last_name': 'f1', 'latitude': '0', 'longitude': '1110',
                'auth_code': 'AA', 'password': 'a', 'role': 'farmer'}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'email': 'aa@a.it', 'first_name': 'f1', 'last_name': 'f1', 'latitude': '1000', 'longitude': '0',
                'auth_code': 'AA', 'password': 'a', 'role': 'farmer'}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # try farmer request with not existent aut_code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'email': 'aa@a.it', 'first_name': 'f1', 'last_name': 'f1', 'latitude': '0', 'longitude': '0',
                'auth_code': 'AAA', 'password': 'a', 'role': 'farmer'}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # try farmer request with invalid aut_code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'email': 'aa@a.it', 'first_name': 'f1', 'last_name': 'f1', 'latitude': '0', 'longitude': '0',
                'auth_code': 'BB', 'password': 'a', 'role': 'farmer'}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # try farmer request with misspelled role
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'email': 'aa@a.it', 'first_name': 'f1', 'last_name': 'f1', 'latitude': '0', 'longitude': '0',
                'auth_code': 'AA', 'password': 'a', 'role': 'farmerr'}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # try farmer request with not assigned role
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'email': 'aa@a.it', 'first_name': 'f1', 'last_name': 'f1', 'latitude': '0', 'longitude': '0',
                'auth_code': 'AA', 'password': 'a', 'role': 'policymaker'}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # correct farmer sigup
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'email': 'aa@a.it', 'first_name': 'f1', 'last_name': 'f1', 'latitude': '0', 'longitude': '0',
                'auth_code': 'AA', 'password': 'a', 'role': 'farmer'}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_policymaker_signup(self):
        url = reverse('users:user_create')

        # request with invalid first name and last name
        data = {'email': 'apa@a.it', 'first_name': 'f11', 'last_name': 'f1', 'latitude': '0', 'longitude': '0',
                'auth_code': 'PP', 'password': 'a', 'role': 'policymaker'}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'email': 'apa@a.it', 'first_name': 'f1', 'last_name': 'f11', 'latitude': '0', 'longitude': '0',
                'auth_code': 'PP', 'password': 'a', 'role': 'policymaker'}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #  request with not existent aut_code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'email': 'apa@a.it', 'first_name': 'f1', 'last_name': 'f1', 'latitude': '0', 'longitude': '0',
                'auth_code': 'AAA', 'password': 'a', 'role': 'policymaker'}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #  request with invalid aut_code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'email': 'apa@a.it', 'first_name': 'f1', 'last_name': 'f1', 'latitude': '0', 'longitude': '0',
                'auth_code': 'BB', 'password': 'a', 'role': 'policymaker'}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # request with misspelled role
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'email': 'apa@a.it', 'first_name': 'f1', 'last_name': 'f1', 'latitude': '0', 'longitude': '0',
                'auth_code': 'PP', 'password': 'a', 'role': 'policimaker'}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # correct policymaker sigup
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'email': 'apa@a.it', 'first_name': 'f1', 'last_name': 'f1', 'latitude': '0', 'longitude': '0',
                'auth_code': 'PP', 'password': 'a', 'role': 'policymaker'}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_agronomist_signup(self):
        url = reverse('users:user_create')
        # request with invalid first name and last name
        data = {'email': 'apa@a.it', 'first_name': 'f11', 'last_name': 'f1', 'latitude': '0', 'longitude': '0',
                'auth_code': 'PP', 'password': 'a', 'role': 'agronomist'}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_string_conversion(self):
        self.assertEqual(str(self.dis1), 'd1')
        self.assertEqual(str(self.ar1), 'a1')
        self.assertEqual(str(self.aF1), 'AA')
        self.assertEqual(str(self.aP1), 'PP')
        self.assertEqual(str(self.aAG1), 'GG')

    def test_info_user(self):
        url = reverse('users:user_info')

        # info about anonymous user
        request = self.factory.get(url)
        response = user_info(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

        # info about farmer
        request = self.factory.get(url)
        force_authenticate(request, user=self.f1)
        response = user_info(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data)[0],
                         {'first_name': 'fname', 'last_name': 'lname', 'role': 'farmer', 'email': 'test@a.it',
                          'area_id': 1, 'district_id': None})
        # info about policymakers
        request = self.factory.get(url)
        force_authenticate(request, user=self.p1)
        response = user_info(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data)[0],
                         {'first_name': 'pfname', 'last_name': 'plname', 'role': 'policymaker', 'email': 'ptest@a.it',
                          'area_id': None, 'district_id': 1})

    def test_user_sign_in_out(self):
        url = reverse('token_obtain_pair')
        url_sup = reverse('users:user_create')
        view = MyTokenObtainPairView.as_view()

        """self.f2 = CustomUser.objects.create(
            email='f2@g.it',
            user_name='f2@g.it',
            first_name='f2e',
            last_name='f2',
            auth_code='BB',
            password='a',
            latitude=10,
            longitude=10,
            area=self.ar1,
            role='farmer'
        )
        self.f1.groups.add(self.group_farmer)
        self.f1.save()"""
        self.aF2 = AuthCodeFarmer(
            code='QQQQ',
            first_name='f2',
            last_name='f2',
            area=self.ar1,
            isValid=True,
        )
        self.aF2.save()

        # Authentication with token invalid credentials
        data = {'email': '10', 'password': 'aa'}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authentication correct data
        data = {'email': 'qqaa@a.it', 'first_name': 'f2', 'last_name': 'f2', 'latitude': '0', 'longitude': '0',
                'auth_code': 'QQQQ', 'password': 'a', 'role': 'farmer'}
        response = self.client.post(path=url_sup, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {'email': 'qqaa@a.it', 'password': 'a'}
        request = self.factory.post(url, data, format='json')
        # force_authenticate(request, user=self.f1)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
