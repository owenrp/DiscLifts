from __future__ import absolute_import
import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
# from DiscLifts_prj.userprofile.models import UserProfile

from .models import Events, Posts, User
# from ..userprofile.models import UserProfile


def create_test_event():
    """
    Returns an event for use with testing.
    :return:
    """
    event_test = Events.objects.create(title='Testing event',
                                       location='Test location',
                                       start_date=timezone.now() + datetime.timedelta(days=30),
                                       end_date=timezone.now() + datetime.timedelta(days=33),
                                       user_id=1,
                                       content='Test content')
    return event_test


def create_test_post(event_id):
    """
    Creates a test post.
    :param event_id: the event the post is for.
    :return:
    """
    post_test = Posts.objects.create(location='test location',
                                     lift_type='I have space',
                                     leaving_time='test leaving time',
                                     spaces=4,
                                     comments='test comments',
                                     leaving_date=timezone.now() + datetime.timedelta(days=30),
                                     event_id=event_id,
                                     user_id=1,
                                     )

    return post_test


class PostsViewTests(TestCase):
    def test_index_view(self):
        """
        Basic test for index page.
        """
        # self.client.get(<URL>) in this case we can use reverse to engineer the url for us.
        response = self.client.get(reverse('posts:index'))
        # .status_code returns the status code from the client response, 200 - successful request.
        self.assertEqual(response.status_code, 200)
        # assertContains will check for a string of text in the html that has been returned from the client request.
        self.assertContains(response, 'Upcoming events')

    def test_events_view(self):
        """
        Basic test for events page.
        """
        # self.client.get(<URL>) in this case we can use reverse to engineer the url for us.
        response = self.client.get(reverse('posts:events'))
        # .status_code returns the status code from the client response, 200 - successful request.
        self.assertEqual(response.status_code, 200)
        # assertContains will check for a string of text in the html that has been returned from the client request.
        self.assertContains(response, 'Upcoming events')

    def test_event_posts_view(self):
        """
        Basic test for event posts page.
        :return:
        """
        event_test = create_test_event()
        # response = self.client.get('/events/{}/'.format(str(event_test.id)))
        response = self.client.get(reverse('posts:event_posts', args=[event_test.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'View event info')

    # Fails but don't know why. Issue #1 in github
    # def test_posts_view(self):
    #     """
    #     Basic test for an individual post.
    #     :return:
    #     """
    #     event_test = create_test_event()
    #     post_test = create_test_post(event_test.id)
    #     # response = self.client.get('/events/posts/{}/'.format(str(post_test.id)))
    #     response = self.client.get(reverse('posts:posts', args=[post_test.id]))
    #
    #     # self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'Posted by')

    def test_past_events_view(self):
        """
        Basic test for past events page.
        :return:
        """
        response = self.client.get(reverse('posts:past_events'))
        self.assertEqual(response.status_code, 200)

    def test_events_user_view(self):
        """
        Basic test for events user page.
        :return:
        """
        user = User.objects.create_user('test')
        response = self.client.get(reverse('posts:events_user', args=[user.id]))
        self.assertEqual(response.status_code, 200)

    def test_how_it_works_view(self):
        """
        Basic test for how it works page.
        :return:
        """
        response = self.client.get(reverse('posts:how_it_works'))
        self.assertEqual(response.status_code, 200)

    def test_add_post_no_login(self):
        """
        Test should redirect user to automatic login page as users have to be signed in to view this view.
        """
        response = self.client.get('/add_post/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Allauth login template')

    # def test_add_post_logged_in(self):
    #     """
    #     Add post page should appear.
    #     :return:
    #     """
    #     self.user = User.objects.create_user(username="test", email="test@test.com", password="test")
    #     self.userprofile = UserProfile.objects.get(pk=self.user.id)
    #     self.client.login(username='test', password='test')
    #     response = self.client.get('/add_post/', follow=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'Add post template')

# def test__view(self):
#     response = self.client.get(reverse('posts:'))
#     self.assertEqual(response.status_code, 200)

