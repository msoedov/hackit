from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework.test import APIClient
# from rest_framework.test import force_authenticate

# from ..serializers import FileSerializer

from .test_models import UserFactory


class TestUserView(TestCase):

    def setUp(self):
        self.admin = UserFactory(password='hallo', username='admin')
        self.admin.save()
        self.client = APIClient()

    def test_as_a_user_i_want_to_see_my_files(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('file-list'))
        self.assertEqual(response.status_code, 200)

    def test_as_an_anonymous_user_i_should_see_nothing(self):
        response = self.client.get(reverse('file-list'))
        self.assertEqual(response.status_code, 403)

    def test_i_can_upload(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(reverse('file-detail', kwargs={'name': 'virus.exe'}),
                                   data=b'Hallo!', content_type='application/jpg')
        self.assertEqual(response.status_code, 200)

    def test_i_can_download(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.put(reverse('file-detail', kwargs={'name': 'virus.exe'}),
                                   data=b'Hallo!', content_type='application/jpg')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('download', kwargs={'name': 'virus.exe'}))
        self.assertEqual(response.status_code, 200)

    def test_file_security(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.put(reverse('file-detail', kwargs={'name': 'virus.exe'}),
                                   data=b'Hallo!', content_type='application/jpg')
        self.assertEqual(response.status_code, 200)

        hacker = UserFactory()
        hacker.save()
        self.client.force_authenticate(user=hacker)
        response = self.client.get(reverse('download', kwargs={'name': 'virus.exe'}))
        self.assertEqual(response.status_code, 404)

    def test_i_can_upload_multiple_times(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(reverse('file-detail', kwargs={'name': 'windows.exe'}), data=b'Hallo!',
                                   content_type='application/jpg')
        self.assertEqual(response.status_code, 200)

        response = self.client.put(reverse('file-detail', kwargs={'name': 'windows.exe'}),
                                   data=b'Never gonna happen!', content_type='application/jpg')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('download', kwargs={'name': 'windows.exe'}))
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.content, b'Never gonna happen!')

    def test_i_can_upload_unicode(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(reverse('file-detail', kwargs={'name': 'вирус.exe'}),
                                   data=b'Hallo!', content_type='application/jpg')
        self.assertEqual(response.status_code, 200)
