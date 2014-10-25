# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0002_link_t4k_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='t4k_url',
            field=models.CharField(max_length=150, null=True, verbose_name=b'T4K URL', blank=True),
        ),
    ]
