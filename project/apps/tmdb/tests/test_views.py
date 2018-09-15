from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APITestCase

from project.apps.accounts.models import User

from ..models import Progress
from ..serializers import ProgressSerializer
from ..views import ProgressViewSet


class ProgressViewSetTests(APITestCase):
    def setUp(self):
        self.viewset = ProgressViewSet

    def test_subclass(self):
        self.assertTrue(issubclass(self.viewset, mixins.CreateModelMixin))
        self.assertTrue(issubclass(self.viewset, mixins.UpdateModelMixin))
        self.assertTrue(issubclass(self.viewset, mixins.DestroyModelMixin))
        self.assertTrue(issubclass(self.viewset, mixins.ListModelMixin))
        self.assertTrue(issubclass(self.viewset, viewsets.GenericViewSet))

    def test_permission_classes(self):
        self.assertEqual(self.viewset.permission_classes, [IsAuthenticated])

    def test_serializer_class(self):
        self.assertEqual(self.viewset.serializer_class, ProgressSerializer)

    def test_lookup_field(self):
        self.assertEqual(self.viewset.lookup_field, 'show_id')


class ProgressViewSetCreateTests(APITestCase):
    def setUp(self):
        self.url = '/tmdb/progress/'
        self.user_1 = User.objects.create_user('u1@test.com', 'foo123')
        self.user_2 = User.objects.create_user('u2@test.com', 'foo123')
        self.client.force_authenticate(user=self.user_1)
        self.data = {
            'show_id': 1,
            'show_name': 'Vikings',
            'show_status': Progress.RETURNING
        }

    def test_201(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Progress.objects.count(), 1)
        self.assertEqual(Progress.objects.filter(user=self.user_1, show_id=1).count(), 1)


class ProgressViewSetUpdateTests(APITestCase):
    def setUp(self):
        self.url = '/tmdb/progress/{}/'
        self.user_1 = User.objects.create_user('u1@test.com', 'foo123')
        self.user_2 = User.objects.create_user('u2@test.com', 'foo123')
        self.client.force_authenticate(user=self.user_1)
        self.progress = Progress.objects.create(user=self.user_1, show_id=1, show_name='Vikings')
        self.data = {
            'show_status': Progress.ENDED
        }

    def test_200(self):
        response = self.client.patch(self.url.format(self.progress.show_id), data=self.data)
        self.assertEqual(response.status_code, 200)
        self.progress.refresh_from_db()
        self.assertEqual(self.progress.user, self.user_1)
        self.assertEqual(self.progress.show_id, 1)
        self.assertEqual(self.progress.show_name, 'Vikings')
        self.assertEqual(self.progress.show_status, Progress.ENDED)


class ProgressViewSetDestroyTests(APITestCase):
    def setUp(self):
        self.url = '/tmdb/progress/{}/'
        self.user_1 = User.objects.create_user('u1@test.com', 'foo123')
        self.user_2 = User.objects.create_user('u2@test.com', 'foo123')
        self.progress_1 = Progress.objects.create(user=self.user_1, show_id=1, show_name='Vikings')
        self.progress_2 = Progress.objects.create(user=self.user_2, show_id=1, show_name='Vikings')

    def test_204_1(self):
        self.client.force_authenticate(user=self.user_1)
        response = self.client.delete(self.url.format(1))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Progress.objects.filter(user=self.user_1).count(), 0)
        self.assertEqual(Progress.objects.filter(user=self.user_2).count(), 1)

    def test_204_2(self):
        self.client.force_authenticate(user=self.user_2)
        response = self.client.delete(self.url.format(1))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Progress.objects.filter(user=self.user_1).count(), 1)
        self.assertEqual(Progress.objects.filter(user=self.user_2).count(), 0)


class ProgressViewSetListTests(APITestCase):
    def setUp(self):
        self.url = '/tmdb/progress/list/'
        self.user_1 = User.objects.create_user('u1@test.com', 'foo123')
        self.user_2 = User.objects.create_user('u2@test.com', 'foo123')
        Progress.objects.create(user=self.user_1, show_id=1, show_name='Vikings')
        Progress.objects.create(user=self.user_1, show_id=2, show_name='Shooter')
        Progress.objects.create(user=self.user_2, show_id=3, show_name='Better Call Saul')

    def test_200_1(self):
        self.client.force_authenticate(user=self.user_1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['show_id'], 2)
        self.assertEqual(response.data[1]['show_id'], 1)

    def test_200_2(self):
        self.client.force_authenticate(user=self.user_2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['show_id'], 3)
