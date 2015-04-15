# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0003_auto_20141024_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='kintera_id',
            field=models.IntegerField(verbose_name=b'Kintera ID', blank=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='last_click',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'Last Clicked'),
        ),
        migrations.AlterField(
            model_name='link',
            name='t4k_url',
            field=models.CharField(max_length=150, null=True, verbose_name=b'T4K Profile Link', blank=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='url',
            field=models.CharField(max_length=50, verbose_name=b'Short Link'),
        ),
        migrations.AlterField(
            model_name='link',
            name='user',
            field=models.ForeignKey(verbose_name=b'Rider', to=settings.AUTH_USER_MODEL),
        ),
    ]
