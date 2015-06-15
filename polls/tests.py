import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from polls.models import Poll

class PollTests(TestCase):

    def test_was_pub_recent_with_future_poll(self):
        """ test """
        future_poll = Poll(published=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_poll.was_published_recently(), False)

    def test_was_pub_recent_with_old_poll(self):
        """ test """
        old_poll = Poll(published=timezone.now() - datetime.timedelta(days=30))
        self.assertEqual(old_poll.was_published_recently(), False)

    def test_was_pub_recent_with_recent_poll(self):
        """ test """
        poll = Poll(published=timezone.now() - datetime.timedelta(hours=1))
        self.assertEqual(poll.was_published_recently(), True)

def create_poll(question, days):
    """ factory - not used yet """
    return Poll.objects.creat(question=question, published=timezone.now() +
        datetime.timedelta(days=days))

class PollViewTests(TestCase):
    
    def test_index_view_with_no_polls(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available")
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])    


