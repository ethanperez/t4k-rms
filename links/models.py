from django.db import models
from datetime import datetime, timedelta
from durationfield.db.models.fields.duration import DurationField
from riders.models import Teammate
from django.utils import timezone

class Link(models.Model):
	user = models.ForeignKey('riders.Teammate', verbose_name = "Rider")
	kintera_id = models.IntegerField('Kintera ID', blank = True)
	url = models.CharField('Short Link', max_length = 50)
	t4k_url = models.CharField('T4K Profile Link', max_length = 150, blank = True, null = True)
	clicks = models.IntegerField(default = 0)
	last_click = models.DateTimeField('Last Clicked', auto_now_add = True)

	class Meta:
		verbose_name = 'link'
		verbose_name_plural = 'links'

	# Base unicode method
	def __unicode__(self):
		# Return the short url
		return self.url
