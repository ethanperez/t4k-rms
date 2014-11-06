# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_link', models.CharField(max_length=50, verbose_name=b'Short Link')),
                ('url', models.CharField(max_length=250, verbose_name=b'Target Link')),
                ('clicks', models.IntegerField(default=0)),
                ('last_click', models.DateTimeField(auto_now_add=True, verbose_name=b'last clicked')),
            ],
            options={
                'verbose_name': 'link',
                'verbose_name_plural': 'links',
            },
            bases=(models.Model,),
        ),
    ]
