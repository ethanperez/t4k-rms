# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kintera_id', models.IntegerField(blank=True)),
                ('url', models.CharField(max_length=50, verbose_name=b'short URL')),
                ('clicks', models.IntegerField(default=0)),
                ('last_click', models.DateTimeField(auto_now_add=True, verbose_name=b'last clicked')),
                ('user', models.ForeignKey(verbose_name=b'link', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'link',
                'verbose_name_plural': 'links',
            },
            bases=(models.Model,),
        ),
    ]
