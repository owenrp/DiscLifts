from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from .models import User, UserProfile

class UserprofileViewTests(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")
        self.userprofile = UserProfile.objects.get(pk=self.user.id)

    def test_profile_view_not_logged_in(self):
        """
        Test should redirect user to automatic login page as users have to be signed in to view this view.
        """
        # arg follow=True means the page follows through any redirection
        response = self.c.get('/user/profile/1', follow=True)
        #print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Allauth login template')


    def test_profile_view_user_logged_in(self):
        """
        Test should show the profile page for the created test user.
        """
        self.c.login(username='test', password='test')
        response = self.c.get('/user/profile/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'View all events from')

    def test_edit_profile_not_logged_in(self):
        """
        Test should redirect user to automatic login page as users have to be signed in to view this view.
        """
        response = self.c.get('/user/update_profile/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Allauth login template')

    def test_edit_profile_user_logged_in(self):
        """
        Test should show the edit profile page for the created test user.
        """
        self.c.login(username='test', password='test')
        response = self.c.get('/user/update_profile/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'update your profile')



        #self.userprofile = UserProfile.objects.get(pk=self.user.id)
        # response = self.client.get('user:profile', args=[self.userprofile.user_id])
        # UserProfile.objects.create(user_id=self.user.id)
        # self.c.login(username='test', password='test')
        # response = self.c.get(reverse('entry_create'))
        # self.assertEqual(response.status_code, 200)

        # def test_profile_view(self):
        #     """
        #     Basic test to check view shows
        #     :return:
        #     """
        #     test_user = create_test_user()
        #     # test_userprofile = UserProfile.objects.create(user_id=test_user.id)
        #
        #     test_userprofile = UserProfile.objects.get(id=test_user.id)
        #     self.client.post('/accounts/login/', {'username': 'test', 'passwd': 'testpw'})
        #     response = self.client.get('user:profile', args=[test_userprofile.user_id])
        #     self.assertEqual(response.status_code, 200)
