from django.test import TestCase, Client

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory
from riders.models import Teammate
from fitness.models import Ride
from dashboard.views import log_ride
from django.core.urlresolvers import reverse

class DashboardViews(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = Teammate.objects.create_user( 'derp@derp.com', 'first', 'last', '2014-01-02', 'top_secret_pass')
        self.second_user = Teammate.objects.create_user( 'derpette@derp.com', 'first', 'last', '2014-01-02', 'top_secret_pass')


    def test_logging_in_successfully(self):
        c = Client()
        args = {'username' : 'derp@derp.com', 'password' : 'top_secret_pass'}
        response = c.post(reverse('dashboard:login'), args)
        self.assertTrue(response.status_code, 302)
        # TODO: hack, this test sucks
        self.assertTrue(response.url.endswith(reverse('dashboard:dashboard')))

    def test_inactive_user(self):
        c = Client()
        self.user.is_active = False
        self.user.save()
        args = {'username' : 'derp@derp.com', 'password' : 'top_secret_pass'}
        response = c.post(reverse('dashboard:login'), args)
        self.assertTrue(response.status_code, 200)
        self.assertTrue(response.context['error_message'], "You're not an active rider, man.")
        self.user.is_active = True
        self.user.save()


    def test_log_ride(self):
        # create an instance of the post request
        args = { 'partners' : "parth", 'miles' : 10, 'pace' : 10, 'time': "01:01:01", 'comments' : 'haderp', 'date' : '2014-01-25' }
        request = self.factory.post('/log/ride', args)

        # simulate login since we don't have access to middleware
        request.user = self.user
        num_rides = Ride.objects.count()

        # "run" the request, as it were
        response = log_ride(request)

        # assert a redirect to the original dashboard
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard:dashboard'))
        self.assertEqual(Ride.objects.count() - num_rides, 1)

    def test_log_ride_time_format(self):
        # create an instance of the post request
        args = { 'partners' : "parth", 'miles' : 10, 'pace' : 10, 'time': "01:01", 'comments' : 'haderp', 'date' : '2014-01-25' }
        request = self.factory.post('/log/ride', args)

        # simulate login since we don't have access to middleware
        request.user = self.user
        num_rides = Ride.objects.count()

        # "run" the request, as it were
        response = log_ride(request)

        # assert it goes to the page again and no rides added
        # TODO this isn't good enough
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ride.objects.count(), num_rides)

    def test_log_ride_escaped_chars(self):
        # create an instance of the post request
        args = { 'partners' : "parth&&''", 'miles' : 10, 'pace' : 10, 'time': "01:01:01", 'comments' : 'abcde!!&&', 'date' : '2014-01-25' }
        request = self.factory.post('/log/ride', args)

        self.assertTrue(Ride.objects.count() == 0)
        # simulate login since we don't have access to middleware
        request.user = self.user
        num_rides = Ride.objects.count()

        # "run" the request, as it were
        response = log_ride(request)

        # assert a redirect to the original dashboard
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard:dashboard'))
        r = Ride.objects.first()
        self.assertEqual(r.comments, "abcde!!&&")
        self.assertEqual(r.buddies, "parth&&''")
        self.assertEqual(Ride.objects.count() - num_rides, 1)

    def test_dashboard_not_logged_in(self):
        # TODO: this behavior is going to change most definitely
        # with no one logged in, it should prompt you to log in
        c = Client()
        response = c.get(reverse('dashboard:dashboard'))
        self.assertTrue(response.url.endswith('login/'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_logged_in(self):
        # with someone logged in, it should show them their own miles
        c = Client()
        c.login(username='derp@derp.com', password='top_secret_pass')
        response = c.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.context['rider'], self.user)

    def test_dashboard_logged_in_with_args(self):
        # with someone logged in and args provided, it should use the args
        c = Client()
        c.login(username='derpette@derp.com', password='top_secret_pass')
        response = c.get(reverse('dashboard:dashboard'), rider=self.second_user.pk)
        self.assertEqual(response.context['rider'], self.second_user)

    def test_password_change(self):
        c = Client()
        c.login(username='derp@derp.com', password='top_secret_pass')
        args = { 'password1' : '&!new_pass', 'password2' : '&!new_pass' }
        c.post(reverse('dashboard:change_password'), args)
        c.logout()
        result = c.login(username='derp@derp.com', password='top_secret_pass')
        self.assertFalse(result)
        result = c.login(username='derp@derp.com', password='&!new_pass')
        self.assertTrue(result)

    def test_different_passwords_change(self):
        c = Client()
        c.login(username='derp@derp.com', password='top_secret_pass')
        args = { 'password1' : 'garbage', 'password2' : 'new_pass' }
        response = c.post(reverse('dashboard:change_password'), args)
        self.assertEqual(response.context['error_message'], "Your passwords don't match!")

