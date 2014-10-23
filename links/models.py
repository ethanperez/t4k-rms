from django.db import models
from datetime import datetime, timedelta
from durationfield.db.models.fields.duration import DurationField
from riders.models import Teammate
from django.utils import timezone

class Link(models.Model):
	user = models.ForeignKey('riders.Teammate', verbose_name = "link")
	kintera_id = models.IntegerField(blank = True)
	url = models.CharField('short URL', max_length = 50)
	clicks = models.IntegerField(default = 0)
	last_click = models.DateTimeField('last clicked', auto_now_add = True)

	class Meta:
		verbose_name = 'link'
		verbose_name_plural = 'links'

	# Base unicode method
	def __unicode__(self):
		# Return the short url
		return self.url
