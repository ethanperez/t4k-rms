from django.contrib import admin
from fitness.models import Ride

# Settings for ride admin
class RideAdmin(admin.ModelAdmin):

    # Fields to list
    list_display = ('user', 'date', 'duration', 'miles', 'pace', 'buddies', 'time_logged')
    # Fields to allow filtering by
    list_filter = ('date',)
    # Fields to seach in with search bay
    search_fields = ('user__first_name', 'user__last_name')
    # Fields to order by
    ordering = ('-time_logged', 'date', 'miles', 'duration', 'pace')

# Add rides to admin panel
admin.site.register(Ride, RideAdmin)