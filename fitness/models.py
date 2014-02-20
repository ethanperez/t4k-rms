from django.db import models
from datetime import datetime, timedelta
from durationfield.db.models.fields.duration import DurationField
from riders.models import Teammate

# Model to log rides
class Ride(models.Model):
    user = models.ForeignKey('riders.Teammate', verbose_name = 'teammate')
    date = models.DateField('date', help_text = 'Date format: YYYY-MM-DD')
    # TODO what if we made this a list of foreign keys for other riders?
    buddies = models.CharField('ride buddies', max_length = 300)
    miles = models.DecimalField('miles ridden', max_digits = 5, decimal_places = 2)
    pace = models.DecimalField('average pace', max_digits = 3, decimal_places = 1)
    duration = DurationField('time to complete ride', help_text = 'HH:MM:SS format')
    comments = models.TextField('comments')
    time_logged = models.DateTimeField('logged', auto_now_add = True)

    # Method to create a new ride
    def log(cls, user, date, buddies, miles, pace, duration, comments):
        user_data = cls(user = user, date = date, buddies = buddies, miles = miles,
                   pace = pace, duration = duration, comments = comments)
        return user_data

    # Metadata for the visual names
    class Meta:
        verbose_name = 'ride'
        verbose_name_plural = 'rides'

    # Base method returns the teammate's name
    def __unicode__(self):
        # Returns the user foreign key, which calls __unicide__ in auth
        return '%s, %d miles' % (self.user, self.miles)

    # Methods to return model values
    def get_miles(self):
        # Returns the miles ridden
        return self.miles

    def get_date(self):
        # Returns the date the ride was on
        return self.date

    def get_pace(self):
        # Returns the pace for the ride
        return self.pace

    def get_duration(self):
        # Returns the time it took to ride
        return self.duration
        
    def get_logged(self):
        # Return the time the ride was logged at
        return self.time_logged