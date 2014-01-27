from django.test import TestCase, Client

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory
from riders.models import Teammate
from dashboard.views import log_ride
from django.core.urlresolvers import reverse

class DashboardViews(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = Teammate.objects.create_user( 'derp@derp.com', 'first', 'last', '2014-01-02', 'top_secret_pass')

    def test_details(self):

        # create an instance of the post request
        request = self.factory.post('/log/ride', args)

        # simulate login since we don't have access to middleware
        request.user = self.user

        # "run" the request, as it were
        response = log_ride(request)
        # assert a redirect to the original dashboard

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard:dashboard'))

# a sample of how we might test and get access to context.
# def test_log_ride(self):
#     c = Client()
#     self.user = Teammate.objects.create_user( 'derp@derp.com', 'first', 'last', '2014-01-02', 'top_secret_pass')
#     c.login(username='derp@derp.com', password='top_secret_pass')
#     args = { 'partners' : "parth", 'miles' : 10, 'pace' : 10, 'time': "01:01:01", 'comments' : 'haderp', 'date' : '2014-01-25' }
#     response = c.put(reverse('dashboard:log_ride'), args)
#     # now we can do response.context or whatever.
#     import pdb; pdb.set_trace()
