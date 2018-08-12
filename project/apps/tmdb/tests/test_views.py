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


class ProgressViewSetRetrieveTests(APITestCase):
    def setUp(self):
        self.url = '/tmdb/progresses/'
        user_1 = User.objects.create_user('u1@test.com', 'foo123')
        user_2 = User.objects.create_user('u2@test.com', 'foo123')
        self.client.force_authenticate(user=user_1)
        self.progress_1 = Progress.objects.create(user=user_1, show_id=1, show_name='Vikings')
        self.progress_2 = Progress.objects.create(user=user_1, show_id=2, show_name='Shooter')
        Progress.objects.create(user=user_2, show_id=1, show_name='Vikings')

    def test_200(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['show_id'], 2)
        self.assertEqual(response.data[1]['show_id'], 1)
