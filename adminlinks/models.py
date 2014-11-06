from django.db import models

class Link(models.Model):
  short_link = models.CharField('Short Link', max_length = 50)
  url = models.CharField('Target Link', max_length = 250)
  clicks = models.IntegerField(default = 0)
  last_click = models.DateTimeField('last clicked', auto_now_add = True)

  class Meta:
    verbose_name = 'link'
    verbose_name_plural = 'links'

  # Base unicode method
  def __unicode__(self):
    # Return the short link
    return self.short_link