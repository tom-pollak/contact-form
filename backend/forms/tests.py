import copy

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import IntegrityError

from rest_framework.test import APITestCase
from rest_framework import status

from tiers.models import Tier
from .models import Form


class FormTest(APITestCase):
    forms_url = reverse('api:form-list')

    def setUp(self):
        User = get_user_model()
        Tier.objects.create(pk=1, name="Free", no_forms=5, price=0.00)
        self.user = User.objects.create_user(
            pk=1, email='test@user.com', password='foo')
        self.alt_user = User.objects.create_user(
            pk=2, email='testalt@user.com', password='foo')

        self.test_user_credentials = {
            'email': 'test@user.com',
            'password': 'foo',
        }
        self.alt_user_credentials = {
            'email': 'testalt@user.com',
            'password': 'foo',
        }
        self.get_token(self.test_user_credentials)

    def get_token(self, credentials):
        response = self.client.post('/auth/jwt/create/', data=credentials)
        token = response.data['access']
        authorization = 'Bearer ' + token
        self.client.credentials(HTTP_AUTHORIZATION=authorization)

    def test_create_form(self):
        data = {
            'name': 'Test',
            'url': 'https://test.com',
            'test_period': 5
        }
        response = self.client.post(self.forms_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        form_name = self.test_get_forms()
        self.assertEqual(form_name, 'Test')

        data_copy = copy.deepcopy(data)
        data_copy['name'] = 'Test diff'
        response = self.client.post(self.forms_url, data=data_copy)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['url'], 'User already created a form with that url.')

        data_copy = copy.deepcopy(data)
        data_copy['url'] = 'https://test-diff.com'
        response = self.client.post(self.forms_url, data=data_copy)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['name'], 'User already created a form with that name.')

        data_copy = copy.deepcopy(data)
        data_copy['test_period'] = -1
        response = self.client.post(self.forms_url, data=data_copy)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['test_period'][0],
                         'Ensure this value is greater than or equal to 0.')

        data_copy = copy.deepcopy(data)
        data_copy['name'] = 'Test diff 2'
        data_copy['url'] = 'https://test-diff-2.com'
        data_copy['created_by'] = self.alt_user
        data_copy['garbage'] = 'garbage'
        response = self.client.post(self.forms_url, data=data_copy)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['created_by'], 1)

    def test_get_forms(self):
        response = self.client.get(self.forms_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if len(response.data) > 0:
            return response.data[0]['name']

        return None

    def test_update_forms(self):
        data = {
            'name': 'Test',
            'url': 'https://test.com',
        }
        response = self.client.post(self.forms_url, data=data)
        id = response.data['id']
        url = reverse('api:form-detail', kwargs={'pk': id})

        response = self.client.patch(url, data={'name': 'New'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            url, data={'created_by': 2})  # attempt to change owner
        self.assertEqual(response.data['created_by'], 1)

        data = {
            'name': 'Test 2',
            'url': 'https://different-url.com',
        }
        response = self.client.post(self.forms_url, data=data)
        id = response.data['id']
        url = reverse('api:form-detail', kwargs={'pk': id})

        # url is same as prev breaking unique integrity
        response = self.client.put(
            url, data={'name': 'Test 2', 'url': 'https://test.com'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'name': 'Alt test',
            'url': 'https://alt.com',
            'test_period': 5
        }
        self.get_token(self.alt_user_credentials)
        response = self.client.post(self.forms_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        id = response.data['id']
        url = reverse('api:form-detail', kwargs={'pk': id})

        self.get_token(self.test_user_credentials)
        response = self.client.patch(url, data={'name': 'New alt'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_form(self):
        data = {
            'name': 'Test',
            'url': 'https://test.com',
            'test_period': 5
        }
        response = self.client.post(self.forms_url, data=data)
        id = response.data['id']
        url = reverse('api:form-detail', kwargs={'pk': id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_submission(self):
        data = {
            'name': 'Test',
            'url': 'https://test.com',
            'test_period': 5
        }
        response = self.client.post(self.forms_url, data=data)
        id = response.data['id']

        submission_data = {
            'key': 'testkey',
        }
        response = self.client.post(reverse(
            'sub-api:submission-list', kwargs={'form_pk': id}), data=submission_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.get_token(self.alt_user_credentials)
        submission_data['key'] = 'new test key'
        response = self.client.post(reverse(
            'sub-api:submission-list', kwargs={'form_pk': id}), data=submission_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    '''
    def test_retrieve_submission(self):
        data = {
            'name': 'Test',
            'url': 'https://test.com',
            'test_period': 5
        }
        response = self.client.post(self.forms_url, data=data)
        id = response.data['id']

        test_create_submission()

        response  = self.client.post(self.submissions_url, kwargs={'form_pk': id, 'pk': submission_pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_submission(self):
        data = {
            'name': 'Test',
            'url': 'https://test.com',
            'test_period': 5
        }
        response = self.client.post(self.forms_url, data=data)
        id = response.data['id']

        response  = self.client.post(self.submissions_url, kwargs={'form_pk': id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    '''
