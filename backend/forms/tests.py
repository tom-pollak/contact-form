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
    form_data = {
        'name': 'Test',
        'url': 'https://test.com',
        'test_period': 5
    }
    test_user_credentials = {
        'email': 'test@user.com',
        'password': 'foo',
    }
    alt_user_credentials = {
        'email': 'testalt@user.com',
        'password': 'foo',
    }

    def setUp(self):
        User = get_user_model()
        Tier.objects.create(pk=1, name="Free", no_forms=5, price=0.00)
        self.user = User.objects.create_user(
            pk=1, email='test@user.com', password='foo')
        self.alt_user = User.objects.create_user(
            pk=2, email='testalt@user.com', password='foo')

        self.get_token(self.test_user_credentials)

    def get_token(self, credentials):
        response = self.client.post('/auth/jwt/create/', data=credentials)
        token = response.data['access']
        authorization = 'Bearer ' + token
        self.client.credentials(HTTP_AUTHORIZATION=authorization)

    def get_form_detail_url(self, pk):
        return reverse('api:form-detail', kwargs={'pk': pk})

    def get_submission_url(self, pk):
        return reverse(
            'sub-api:submission-list', kwargs={'form_pk': pk}
        )

    def test_get_forms(self):
        response = self.client.get(self.forms_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_form(self):
        response = self.client.post(self.forms_url, data=self.form_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.forms_url)
        self.assertEqual(self.form_data['name'], response.json()[0]['name'])

    def test_create_same_name_url(self):
        self.client.post(self.forms_url, data=self.form_data)
        response = self.client.post(self.forms_url, data=self.form_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()[
                'name'][0], 'You have already created a form with that name'
        )
        # ------------------------------------------------------------------
        # should also return error for url but integrity error in view only
        # does 1 error at a time

    def test_create_form_with_neg_time_period(self):
        data_copy = copy.deepcopy(self.form_data)
        data_copy['test_period'] = -1
        response = self.client.post(self.forms_url, data=data_copy)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['test_period'][0],
                         'Ensure this value is greater than or equal to 0.')

    def test_create_form_with_different_user(self):
        data_copy = copy.deepcopy(self.form_data)
        data_copy['created_by'] = self.alt_user
        response = self.client.post(self.forms_url, data=data_copy)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['created_by'], 1)

    def test_patch_form(self):
        response = self.client.post(self.forms_url, data=self.form_data)
        id = response.data['id']

        response = self.client.patch(
            self.get_form_detail_url(id), data={'name': 'New'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            self.get_form_detail_url(id), data={'created_by': 2})  # attempt to change owner
        self.assertEqual(response.data['created_by'], 1)

        self.get_token(self.alt_user_credentials)
        response = self.client.patch(
            self.get_form_detail_url(id), data={'name': 'New alt'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_form(self):
        alt_form_data = {
            'name': 'Alt test',
            'url': 'https://alt.com',
            'test_period': 5
        }

        response = self.client.post(self.forms_url, data=self.form_data)
        id = response.data['id']

        response = self.client.put(
            self.get_form_detail_url(id), data=alt_form_data)  # change data to alt data
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(self.forms_url, data=self.form_data)
        id = response.data['id']

        # url is same as prev breaking unique integrity
        response = self.client.put(
            self.get_form_detail_url(id), data=alt_form_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_form(self):
        data = {
            'name': 'Test',
            'url': 'https://test.com',
            'test_period': 5
        }
        response = self.client.post(self.forms_url, data=data)
        id = response.data['id']

        response = self.client.delete(self.get_form_detail_url(id))
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
        response = self.client.post(
            self.get_submission_url(id), data=submission_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.get_token(self.alt_user_credentials)
        response = self.client.post(
            self.get_submission_url(id), data=submission_data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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

        response  = self.client.post(self.submissions_url, kwargs={
                                     'form_pk': id, 'pk': submission_pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_submission(self):
        data = {
            'name': 'Test',
            'url': 'https://test.com',
            'test_period': 5
        }
        response = self.client.post(self.forms_url, data=data)
        id = response.data['id']

        response  = self.client.post(
            self.submissions_url, kwargs={'form_pk': id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    '''
