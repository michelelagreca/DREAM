from unicodedata import category
from django.test import TestCase
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase, APIRequestFactory, force_authenticate
from django.contrib.auth.models import Group


from forum.models import Category
from users.models import CustomUser, District, Area
from report.models import HarvestReport
from report_api.views import ReportList
from datetime import datetime

class MessagesTestes(APITestCase):
    def setUp(self):
        
        self.factory = APIRequestFactory()  # used to perform CRUD operations
        self.group_farmer = Group(name='farmer-group')
        self.group_policymaker = Group(name='policymaker-group')
        self.group_farmer.save()
        self.group_policymaker.save()

        self.district1 = District( # district 1
            name='district1'
        )
        self.district1.save()

        self.area1 = Area( # area 1
            name='area1',
            district=self.district1
        )
        self.area1.save()

        self.f1 = CustomUser.objects.create( # farmer 1
            email='a@a.it',
            user_name='a@a.it',
            first_name='a',
            last_name='a',
            auth_code='a',
            password='a',
            latitude=1,
            longitude=1,
            area_id=self.area1.id
        )
        self.f1.groups.add(self.group_farmer)
        self.f1.save()

        self.p1 = CustomUser.objects.create( # policy maker 1
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


        self.cat1 = Category( # category 1
            name='c1'
        )
        self.cat1.save()

        self.r1 = HarvestReport(
            firstName='r',
            lastName='r',
            date=datetime.now(),
            area=self.area1,
            category=self.cat1,
            cropName='r',
            quantity='4',
            genericProblems='r',
            weatherProblems='r',
            author=self.f1
        )


    def test_list_tip_category(self):
        url = reverse('report_api:reportlist')
        
        
        # try access with unauthorized user policymaker
        request = self.factory.get(url)
        force_authenticate(request, user=self.p1)
        response = ReportList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # normal flow
        request = self.factory.get(url)
        force_authenticate(request, user=self.f1)
        response = ReportList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

