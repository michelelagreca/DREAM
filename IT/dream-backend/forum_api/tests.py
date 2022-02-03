from django.test import TestCase
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase, APIRequestFactory, force_authenticate
from django.contrib.auth.models import Group

from forum.models import Question, Tip, Answer, Category
from forum_api.views import question_add, tip_add, answer_add, answer_list, tip_list, question_list, CategoryList
from users.models import CustomUser, District, Area


class MessagesTestes(APITestCase):
    def setUp(self):
        """
        Context:
            farmers: f1,f2,f3
            policymakers: p1
            Category: c1
            Question: q1
            Tip: t1
            Answer: a1
            
        """
        self.factory = APIRequestFactory()  # used to perform CRUD operations
        self.group_farmer = Group(name='farmer-group')
        self.group_policymaker = Group(name='policymaker-group')
        self.group_farmer.save()
        self.group_policymaker.save()

        self.f1 = CustomUser.objects.create( # farmer 1
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

        self.f2 = CustomUser.objects.create( # farmer 2
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

        self.f3 = CustomUser.objects.create( # farmer 3
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

        self.district1 = District( # district 1
            name='district1'
        )
        self.district1.save()

        self.area1 = Area( # area 1
            name='area1',
            district=self.district1
        )
        self.area1.save()

        self.cat1 = Category( # category 1
            name='c1'
        )

        self.cat1.save()

        self.q1 = Question.objects.create( # question 1
            title="q1",
            text_body="q1",
            area=self.area1,
            category=self.cat1,
            author=self.f1
        )
        self.q1.save()

        self.t1 = Tip.objects.create( # tip 1
            title="t1",
            text_body="t1",
            area=self.area1,
            category=self.cat1,
            author=self.f1,
            is_star=False
        )
        self.t1.save()

        self.a1 = Answer.objects.create( # answer 1
            question=self.q1,
            text_body="a1",
            author=self.f1
        )
        self.a1.save()




    def test_list_questions(self):
        url = reverse('forum_api:questionlistcreate')
        """
        Normal flow
        """
        request = self.factory.get(url)
        force_authenticate(request, user=self.f1)
        response = question_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)




    def test_list_tips(self):
        url = reverse('forum_api:tiplistcreate')
        """
        Normal flow
        """
        request = self.factory.get(url)
        force_authenticate(request, user=self.f1)
        response = tip_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)





    def test_list_answers(self):
        url = reverse('forum_api:answer_list')
        """
        Normal flow
        """
        request = self.factory.get(url + '/?id=1')
        force_authenticate(request, user=self.f1)
        response = answer_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """
        Error in input data
        """
        request = self.factory.get(url)
        force_authenticate(request, user=self.f1)
        response = answer_list(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)





    def test_post_question(self):
        """
        Ensure only farmer can add questions.
        """
        url = reverse('forum_api:questioncreate')

        # try access with unauthorized user policymaker
        request = self.factory.post(url)
        force_authenticate(request, user=self.p1)
        response = question_add(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try correct farmer post (f1)
        # data = {'title': self.q1.title, 'text_body': self.q1.text_body, 'category': self.cat1.name, 'area': self.area1.name, 'author': self.f1.id}
        # request = self.factory.post(url, data, format='json')
        # force_authenticate(request, user=self.f1)
        # response = question_add(request)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # try to send message (f1 f2) and verify it's saved
        # data = {'reference_hr': self.hr1.id, 'body': 'aa'}
        # request = self.factory.post(url, data, format='json')
        # force_authenticate(request, user=self.f1)
        # response = hr_message_add(request)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # request = self.factory.get(url + '/?id=1')
        # force_authenticate(request, user=self.f1)
        # response = hr_message_list(request)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 3)  # +1 message


        # force_authenticate(request, user=self.f2)
        # response = hr_message_list(request)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 2)

        # # try unauthorized farmer request (f3)
        # request = self.factory.get(url + '/?id=1')
        # force_authenticate(request, user=self.f3)
        # response = hr_message_list(request)
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # # try get not existing message list
        # request = self.factory.get(url + '/?id=2')
        # force_authenticate(request, user=self.f1)
        # response = hr_message_list(request)
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_tip(self):
        """
        Ensure only farmer can add tips.
        """
        url = reverse('forum_api:tipcreate')

        # try access with unauthorized user policymaker
        request = self.factory.post(url)
        force_authenticate(request, user=self.p1)
        response = tip_add(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # # try farmer request without id of the hr
        # request = self.factory.get(url)
        # force_authenticate(request, user=self.f1)
        # response = hr_message_list(request)
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # # try correct farmer requests (f1 and f2)
        # request = self.factory.get(url + '/?id=1')
        # force_authenticate(request, user=self.f1)
        # response = hr_message_list(request)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # request = self.factory.get(url + '/?id=1')
        # self.assertEqual(len(response.data), 2)

        # force_authenticate(request, user=self.f2)
        # response = hr_message_list(request)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 2)

        # # try unauthorized farmer request (f3)
        # request = self.factory.get(url + '/?id=1')
        # force_authenticate(request, user=self.f3)
        # response = hr_message_list(request)
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # # try get not existing message list
        # request = self.factory.get(url + '/?id=2')
        # force_authenticate(request, user=self.f1)
        # response = hr_message_list(request)
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_answer(self):
        """
        Ensure only farmer can add tips.
        """
        url = reverse('forum_api:answerlistcreate')

        # try access with unauthorized user policymaker
        request = self.factory.post(url)
        force_authenticate(request, user=self.p1)
        response = answer_add(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # # try farmer request without id of the hr
        # request = self.factory.get(url)
        # force_authenticate(request, user=self.f1)
        # response = hr_message_list(request)
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # # try correct farmer requests (f1 and f2)
        # request = self.factory.get(url + '/?id=1')
        # force_authenticate(request, user=self.f1)
        # response = hr_message_list(request)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # request = self.factory.get(url + '/?id=1')
        # self.assertEqual(len(response.data), 2)

        # force_authenticate(request, user=self.f2)
        # response = hr_message_list(request)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 2)

        # # try unauthorized farmer request (f3)
        # request = self.factory.get(url + '/?id=1')
        # force_authenticate(request, user=self.f3)
        # response = hr_message_list(request)
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # # try get not existing message list
        # request = self.factory.get(url + '/?id=2')
        # force_authenticate(request, user=self.f1)
        # response = hr_message_list(request)
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
