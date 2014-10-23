# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import durationfield.db.models.fields.duration
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(help_text=b'Date format: YYYY-MM-DD', verbose_name=b'date')),
                ('buddies', models.CharField(max_length=300, verbose_name=b'ride buddies')),
                ('miles', models.DecimalField(verbose_name=b'miles ridden', max_digits=5, decimal_places=2)),
                ('pace', models.DecimalField(verbose_name=b'average pace', max_digits=3, decimal_places=1)),
                ('duration', durationfield.db.models.fields.duration.DurationField(help_text=b'HH:MM:SS format', verbose_name=b'time to complete ride')),
                ('comments', models.TextField(verbose_name=b'comments')),
                ('time_logged', models.DateTimeField(auto_now_add=True, verbose_name=b'date logged', null=True)),
                ('user', models.ForeignKey(verbose_name=b'teammate', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ride',
                'verbose_name_plural': 'rides',
            },
            bases=(models.Model,),
        ),
    ]
