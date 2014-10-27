# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teammate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=100, verbose_name=b'email address', db_index=True)),
                ('first_name', models.CharField(max_length=35, verbose_name=b'first name')),
                ('last_name', models.CharField(max_length=35, verbose_name=b'last name')),
                ('title', models.CharField(default=b'Rider', max_length=100, verbose_name=b'title')),
                ('route', models.CharField(max_length=20, choices=[(b'sierra', b'Sierra'), (b'rockies', b'Rockies'), (b'ozarks', b'Ozarks')])),
                ('date_of_birth', models.DateField(help_text=b'YYYY-MM-DD format', verbose_name=b'date of birth')),
                ('is_staff', models.BooleanField(default=False, help_text=b'Designates who may login to the admin area', verbose_name=b'leadership status')),
                ('is_active', models.BooleanField(default=True, help_text=b'Designates whether or not the teammate can login', verbose_name=b'active status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date added')),
                ('first_login', models.BooleanField(default=True, verbose_name=b'has logged in')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'teammate',
                'verbose_name_plural': 'teammates',
            },
            bases=(models.Model,),
        ),
    ]
