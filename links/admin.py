from django.contrib import admin
from links.models import Link

# Settings for link
class LinkAdmin(admin.ModelAdmin):
  
  # Fields to list
  list_display = ('user', 'kintera_id', 't4k_url', 'url', 'clicks', 'last_click')
  # Filter by
  list_filter = ('user', )
  # Fields to order by
  ordering = ('user',)

# Add to admin
admin.site.register(Link, LinkAdmin)