from django.test import TestCase

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory
from riders.models import Teammate
from dashboard.views import log_ride
from django.core.urlresolvers import reverse

#TODO taken almost entirely from the tutorial, need to make better; just a starting point
class SimpleTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = Teammate.objects.create_user( 'derp@derp.com', 'first', 'last', '2014-01-02', 'top_secret_pass')

    def test_details(self):

        # create an instance of the post request
        args = { 'partners' : "parth", 'miles' : 10, 'pace' : 10, 'time': "01:01:01", 'comments' : 'haderp', 'date' : '2014-01-25' }
        request = self.factory.post('/log/ride', args)

        # simulate login since we don't have access to middleware
        request.user = self.user

        # "run" the request, as it were
        response = log_ride(request)
        # assert a redirect to the original dashboard
        # TODO: how do we inspect the 'context' field of the view? can we mock out render or something?
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard:dashboard'))
