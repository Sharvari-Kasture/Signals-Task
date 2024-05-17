from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Post, BlockedUser

class PostTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='otheruser', password='testpassword')
        self.client = APIClient()
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.post = Post.objects.create(title='Test Post', body='Test Body', author=self.user)

    def test_update_post_not_author(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {RefreshToken.for_user(self.user2).access_token}')
        url = reverse('post-detail', args=[self.post.id])
        data = {'title': 'Updated Title', 'body': 'Updated Body'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_post(self):
        url = reverse('post-list-create')
        data = {'title': 'New Post', 'body': 'New Body'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Post')
        self.assertEqual(response.data['body'], 'New Body')
        self.assertEqual(response.data['author'], self.user.username)

    def test_get_posts(self):
        url = reverse('post-list-create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_single_post(self):
        url = reverse('post-detail', args=[self.post.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.post.title)

    def test_update_post(self):
        url = reverse('post-detail', args=[self.post.id])
        data = {'title': 'Updated Title', 'body': 'Updated Body'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')
        self.assertEqual(self.post.body, 'Updated Body')

    def test_delete_post(self):
        url = reverse('post-detail', args=[self.post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.post.refresh_from_db()
        self.assertTrue(self.post.is_deleted)

    def test_create_post_unauthenticated(self):
        self.client.credentials()  # Remove authentication credentials
        url = reverse('post-list-create')
        data = {'title': 'New Post', 'body': 'New Body'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_not_author(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {RefreshToken.for_user(self.user2).access_token}')
        url = reverse('post-detail', args=[self.post.id])
        data = {'title': 'Updated Title', 'body': 'Updated Body'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_not_author(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {RefreshToken.for_user(self.user2).access_token}')
        url = reverse('post-detail', args=[self.post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class BlockedUserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='otheruser', password='testpassword')
        self.client = APIClient()
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_block_user(self):
        url = reverse('block-user')
        data = {'blocked_user': self.user2.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(BlockedUser.objects.filter(user=self.user, blocked_user=self.user2).exists())

    def test_get_blocked_users(self):
        BlockedUser.objects.create(user=self.user, blocked_user=self.user2)
        url = reverse('get-blocked-user')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['blocked_user'], self.user2.id)

    def test_unblock_user(self):
        BlockedUser.objects.create(user=self.user, blocked_user=self.user2)
        url = reverse('unblock-user')
        data = {'blocked_user_id': self.user2.id}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BlockedUser.objects.filter(user=self.user, blocked_user=self.user2).exists())
