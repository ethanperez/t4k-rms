from django.db import models
from django.utils import timezone
# For teammate manager and modification of Django's base user auth system
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Manager class that instantiates the creation of a new teammate
# source (i think): http://procrastinatingdev.com/django/using-configurable-user-models-in-django-1-5/
class TeammateManager(BaseUserManager):

    # Base create teammate method
    def _create_user(self, email, first_name, last_name, date_of_birth, password,
                     is_staff, is_superuser, **extra_fields):
        # Define the time
        now = timezone.now()
        # Check for an email
        if not email:
            # If none, tell the user
            raise ValueError('The teammate must set an email!')

        # Clean and assign data
        email = self.normalize_email(email)
        user = self.model(email = email, is_staff = is_staff,
                          is_active = True, is_superuser = is_superuser,
                          last_login = now, first_name = first_name,
                          last_name = last_name, date_of_birth = date_of_birth,
                          date_joined = now, **extra_fields)
        # Ready to insert into database
        user.set_password(password)
        user.save(using = self._db)

        return user

    # Method to create a normal teammate; has not access to admin panel
    def create_user(self, email, first_name, last_name, date_of_birth, password, **extra_fields):
        # Utilizes the base creation method
        return self._create_user(email, first_name, last_name, date_of_birth, password, False, False, **extra_fields)

    # Method to create a 'superuser'; has access to EVERYTHING
    def create_superuser(self, email, first_name, last_name, date_of_birth, password, **extra_fields):
        # Utilize the base creation method
        return self._create_user(email, first_name, last_name, date_of_birth, password, True, True, **extra_fields)

# Model that holds the teammates' data
class Teammate(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', max_length = 100, unique = True, db_index = True)
    first_name = models.CharField('first name', max_length = 35)
    last_name = models.CharField('last name', max_length = 35)
    title = models.CharField('title', max_length = 100, default = 'Rider')

    ROUTE_CHOICES = (
      ( 'sierra', 'Sierra' ),
      ( 'rockies', 'Rockies' ),
      ( 'ozarks', 'Ozarks' )
    )

    route = models.CharField(max_length=20, choices=ROUTE_CHOICES)
    date_of_birth = models.DateField('date of birth', help_text = 'YYYY-MM-DD format')
    is_staff = models.BooleanField('leadership status', default = False,
                                   help_text = 'Designates who may login to the admin area')
    is_active = models.BooleanField('active status', default = True,
                                    help_text = 'Designates whether or not the teammate can login')
    date_joined = models.DateTimeField('date added', default = timezone.now)
    first_login = models.BooleanField('has logged in', default = True)

    # Defines the class that manages the teammate
    objects = TeammateManager()

    # Defines what field will be used as the username
    USERNAME_FIELD = 'email'
    # Defines what field(s) will be required
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']

    # Metadata about the model
    class Meta:
        verbose_name = 'teammate'
        verbose_name_plural = 'teammates'

    # Methods to return values about the teammate
    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        # Returns the full name
        return full_name.strip()
    get_full_name.short_description = 'Teammate'

    def get_short_name(self):
        # Returns the first name
        return self.first_name

    def get_email(self):
        # Returns the email address
        return self.email

    def get_title(self):
        # Returns the title
        return self.title

    def get_route(self):
        # Returns the route
        return self.route

    def get_dob(self):
        # Returns the DOB
        return self.date_of_birth

    # Base called function
    def __unicode__(self):
        return self.get_full_name()
