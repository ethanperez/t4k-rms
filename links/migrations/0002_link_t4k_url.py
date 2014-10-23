# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='t4k_url',
            field=models.CharField(default=b'http://www.texas4000.org', max_length=150, verbose_name=b'T4K URL', blank=True),
            preserve_default=True,
        ),
    ]
