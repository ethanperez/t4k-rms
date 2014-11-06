from django.contrib import admin
from adminlinks.models import Link

# Settings for admin link 
class LinkAdmin(admin.ModelAdmin):

  # Fields to list
  list_display = ('short_link', 'url', 'clicks', 'last_click')
  # Filter by
  list_filter = ('short_link', 'url', 'clicks', 'last_click')
  # Fields to order by
  ordering = ('-last_click', 'short_link')

# Add links to admin panel
admin.site.register(Link, LinkAdmin)