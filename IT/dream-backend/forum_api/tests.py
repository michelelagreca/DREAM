from unicodedata import category
from django.test import TestCase
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase, APIRequestFactory, force_authenticate
from django.contrib.auth.models import Group
from django.contrib.auth.models import AnonymousUser


from forum.models import Question, Tip, Answer, Category
from forum_api.views import question_add, tip_add, answer_add, answer_list, tip_list, question_list, CategoryList, answer_remove_vote, tip_remove_vote, tip_like, tip_dislike, answer_like, answer_dislike
# from forum_api.views import TipListCategory, TipListArea
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


    '''def test_list_tip_category(self):
        url = reverse('forum_api:tiplistcategory', args=('c1',))
        
        
        # try access with unauthorized user policymaker
        request = self.factory.get(url)
        force_authenticate(request, user=self.p1)
        response = TipListCategory.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)'''

    '''def test_list_tip_area(self):
        url = reverse('forum_api:tiplistarea', args=('c1',))
        
        # try access with unauthorized user policymaker
        request = self.factory.get(url)
        force_authenticate(request, user=self.p1)
        response = TipListArea.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)'''

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

        
        """
        Autolike
        """
        url = reverse('forum_api:tip_like')
        data = {'tip_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_like(request)
        url = reverse('forum_api:tiplistcreate')
        request = self.factory.get(url)
        force_authenticate(request, user=self.f1)
        response = tip_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """
        Autodislike
        """
        url = reverse('forum_api:tip_dislike')
        data = {'tip_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_dislike(request)
        url = reverse('forum_api:tiplistcreate')
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

        """
        Autolike
        """
        url = reverse('forum_api:answer_like')
        data = {'answer_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_like(request)
        url = reverse('forum_api:answer_list')
        request = self.factory.get(url + '/?id=1')
        force_authenticate(request, user=self.f1)
        response = answer_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """
        Autodislike
        """
        url = reverse('forum_api:answer_dislike')
        data = {'answer_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_dislike(request)
        url = reverse('forum_api:answer_list')
        request = self.factory.get(url + '/?id=1')
        force_authenticate(request, user=self.f1)
        response = answer_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)





    def test_post_question(self):
        
        url = reverse('forum_api:questioncreate')

        # try access with unauthorized user policymaker
        request = self.factory.post(url)
        force_authenticate(request, user=self.p1)
        response = question_add(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try access as anonymous
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try invalid data format
        data = {'tile': self.q1.title, 'text_body': self.q1.text_body, 'category': self.q1.category.name, 'area': self.f1.area_id}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = question_add(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # # # try wrong category
        # data = {'title': self.q1.title, 'text_body': self.q1.text_body, 'category': 'c2', 'area': self.f1.area_id}
        # request = self.factory.post(url, data, format='json')
        # force_authenticate(request, user=self.f1)
        # response = question_add(request)
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


        # try correct farmer post (f1)
        data = {'title': self.q1.title, 'text_body': self.q1.text_body, 'category': self.q1.category.name, 'area': self.f1.area_id}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = question_add(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        

    def test_post_tip(self):
       
        url = reverse('forum_api:tipcreate')

        # try access with unauthorized user policymaker
        request = self.factory.post(url)
        force_authenticate(request, user=self.p1)
        response = tip_add(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try access as anonymous
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try invalid data format
        data = {'tile': self.t1.title, 'text_body': self.t1.text_body, 'category': self.t1.category.name, 'area': self.f1.area_id}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_add(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # # try wrong category
        # data = {'title': self.t1.title, 'text_body': self.t1.text_body, 'category': self.t1.category.name, 'area': self.f1.area_id}
        # request = self.factory.post(url, data, format='json')
        # force_authenticate(request, user=self.f1)
        # response = tip_add(request)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)


        # try correct farmer post (f1)
        data = {'title': self.t1.title, 'text_body': self.t1.text_body, 'category': self.t1.category.name, 'area': self.f1.area_id}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_add(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_post_answer(self):
    
        url = reverse('forum_api:answerlistcreate')

        # try access with unauthorized user policymaker
        request = self.factory.post(url)
        force_authenticate(request, user=self.p1)
        response = answer_add(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try access as anonymous
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try invalid data format
        data = {'question': self.p1.district, 'ttle': self.q1.title, 'text_body': self.q1.text_body}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_add(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # # try wrong category
        # data = {'title': self.q1.title, 'text_body': self.q1.text_body, 'category': self.q1.category.name, 'area': self.f1.area_id}
        # request = self.factory.post(url, data, format='json')
        # force_authenticate(request, user=self.f1)
        # response = question_add(request)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)


        # try correct farmer post (f1)
        data = {'question': self.a1.question.id, 'title': self.q1.title, 'text_body': self.q1.text_body}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_add(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        

    def test_tip_like(self):
       
        url = reverse('forum_api:tip_like')

        # try access with unauthorized user policymaker
        request = self.factory.post(url)
        force_authenticate(request, user=self.p1)
        response = tip_like(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try access as anonymous
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try wrong data format
        data = {'tipid': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_like(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # try not existing tip
        data = {'tip_id': "2"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_like(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # try send same like
        data = {'tip_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_like(request)
        data = {'tip_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_like(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # try to send like and dislike same post
        data = {'tip_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_dislike(request)
        data = {'tip_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_like(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # try correct flow
        data = {'tip_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_like(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tip_dislike(self):
       
        url = reverse('forum_api:tip_dislike')

        # try access with unauthorized user policymaker
        request = self.factory.post(url)
        force_authenticate(request, user=self.p1)
        response = tip_dislike(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try access as anonymous
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try wrong data format
        data = {'tipid': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_dislike(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # try not existing tip
        data = {'tip_id': "2"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_dislike(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # try send same dislike
        data = {'tip_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_dislike(request)
        data = {'tip_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_dislike(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # try correct flow
        data = {'tip_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_dislike(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tip_remove_vote(self):
       
        url = reverse('forum_api:tip_remove_vote')

        # try access with unauthorized user policymaker
        request = self.factory.post(url)
        force_authenticate(request, user=self.p1)
        response = tip_remove_vote(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try access as anonymous
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try wrong data format
        data = {'tipid': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_remove_vote(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # try not existing tip
        data = {'tip_id': "2"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_remove_vote(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # try remove a like
        data = {'tip_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_like(request)
        data = {'tip_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_remove_vote(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # try remove a dislike
        data = {'tip_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_dislike(request)
        data = {'tip_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_remove_vote(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # try correct flow
        data = {'tip_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = tip_remove_vote(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_answer_like(self):
       
        url = reverse('forum_api:answer_like')

        # try access with unauthorized user policymaker
        request = self.factory.post(url)
        force_authenticate(request, user=self.p1)
        response = answer_like(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try access as anonymous
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try wrong data format
        data = {'answerid': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_like(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # try not existing answer
        data = {'answer_id': "2"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_like(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # try send same like
        data = {'answer_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_like(request)
        data = {'answer_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_like(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # try to send like and dislike same post
        data = {'answer_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_dislike(request)
        data = {'answer_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_like(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # try correct flow
        data = {'answer_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_like(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_answer_dislike(self):
       
        url = reverse('forum_api:answer_dislike')

        # try access with unauthorized user policymaker
        request = self.factory.post(url)
        force_authenticate(request, user=self.p1)
        response = answer_dislike(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try access as anonymous
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try wrong data format
        data = {'answerid': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_dislike(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # try not existing answer
        data = {'answer_id': "2"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_dislike(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # try send same like
        data = {'answer_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_dislike(request)
        data = {'answer_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_dislike(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # try correct flow
        data = {'answer_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_dislike(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_answer_remove_vote(self):
       
        url = reverse('forum_api:answ_remove_vote')

        # try access with unauthorized user policymaker
        request = self.factory.post(url)
        force_authenticate(request, user=self.p1)
        response = answer_remove_vote(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try access as anonymous
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # try wrong data format
        data = {'answerid': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_remove_vote(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # try not existing answer
        data = {'answer_id': "2"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_remove_vote(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # try remove a like
        data = {'answer_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_like(request)
        data = {'answer_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_remove_vote(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # try remove a dislike
        data = {'answer_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_dislike(request)
        data = {'answer_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_remove_vote(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # try correct flow
        data = {'answer_id': "1"}
        request = self.factory.post(url, data, format='json')
        force_authenticate(request, user=self.f1)
        response = answer_remove_vote(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_category_to_string(self):
        c = Category(
            name='n'
        )
        self.assertEqual(str(c), 'n')

    def test_question_to_string(self):
        q = Question(
            title='n',
            text_body='n',
            author=self.f1,
            category=self.cat1,
            area=self.area1
        )
        self.assertEqual(str(q), 'n')

    def test_tip_to_string(self):
        t = Tip(
            title='t',
            text_body='t',
            author=self.f1,
            category=self.cat1,
            area=self.area1,
            is_star=False
        )
        self.assertEqual(str(t), 't')

    def test_answer_to_string(self):
        a = Answer(
            question=self.q1,
            text_body='a',
            author=self.f1
        )
        self.assertEqual(str(a), 'a')