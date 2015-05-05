# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fortumo', '0002_auto_20150503_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='ips',
            field=json_field.fields.JSONField(default=[], help_text='Enter a valid JSON object'),
        ),
        migrations.AddField(
            model_name='service',
            name='validate_ip',
            field=models.BooleanField(default=True),
        ),
    ]
