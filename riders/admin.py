from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from riders.models import Teammate, Title, Route
from riders.forms import TeammateCreationForm, TeammateChangeForm

class TeammateAdmin(UserAdmin):

    # The forms to add and change user instances
    form = TeammateChangeForm
    add_form = TeammateCreationForm

    # The attributes of each teammate that are displayed
    list_display = ('get_full_name', 'email', 'title', 'route', 'is_staff')
    list_filter = ('is_staff', 'route')

    # Fields that are shown in edit user pane
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Information', {'fields': ('first_name', 'last_name', 'date_of_birth')}),
        ('Team Information', {'fields': ('title', 'route')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                          'user_permissions')}),
    )

    # Fields that are shown in create user pane
    add_fieldsets = (
        (None, {'classes': ('wide,'),
        'fields': ('email', 'first_name', 'last_name', 'title', 'route',
        'date_of_birth', 'password1', 'password2')}
        ),
    )

    # Fields that are searched through search bar
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('first_name', 'last_name')
    filter_horizontal = ('groups', 'user_permissions')

# Take the above mention changes into effect
admin.site.register(Teammate, TeammateAdmin)
admin.site.register(Title)
admin.site.register(Route)
