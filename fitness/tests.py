from django.test import TestCase

from . import models
from riders.models import Teammate

class ManagerTests(TestCase):

    """
    Make sure that the create_user and create_superuser functions on
    TeammateManager work
    """
    def test_regular_instantiation(self):
        self.assertEqual(Teammate.objects.count(), 0)
        Teammate.objects.create_user(
            email = "derp@derp.com",
            first_name = "othan",
            last_name = "peroni",
            password = "such_secret_wow",
            date_of_birth = "2012-04-07"
        )
        self.assertEqual(Teammate.objects.count(), 1)
        tm = Teammate.objects.first()
        self.assertTrue(tm.get_email(), "derp@derp.com")
        self.assertFalse(tm.has_perm('is_supervisor'))
        self.assertFalse(tm.has_perm('is_staff'))

    def test_admin_instatiation(self):
        self.assertEqual(Teammate.objects.count(), 0)
        Teammate.objects.create_superuser(
            email = "derp@derp.com",
            first_name = "othan",
            last_name = "peroni",
            password = "such_secret_wow",
            date_of_birth = "2012-04-07"
        )
        self.assertEqual(Teammate.objects.count(), 1)
        tm = Teammate.objects.first()
        self.assertTrue(tm.get_email(), "derp@derp.com")
        self.assertTrue(tm.has_perm('is_supervisor'))
        self.assertTrue(tm.has_perm('is_staff'))
