# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('message', models.CharField(max_length=64)),
                ('sender', models.CharField(db_index=True, max_length=64)),
                ('country', models.CharField(max_length=2)),
                ('price', models.FloatField()),
                ('price_wo_vat', models.FloatField()),
                ('currency', models.CharField(max_length=3)),
                ('service_id', models.CharField(max_length=128)),
                ('message_id', models.CharField(max_length=128)),
                ('keyword', models.CharField(max_length=64)),
                ('shortcode', models.CharField(max_length=64)),
                ('operator', models.CharField(max_length=128)),
                ('billing_type', models.CharField(max_length=2)),
                ('status', models.CharField(max_length=64)),
                ('test', models.CharField(max_length=16)),
                ('sig', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('pin', models.CharField(max_length=16, unique=True)),
                ('used', models.BooleanField(default=False)),
                ('message', models.OneToOneField(to='fortumo.Message')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('secret', models.CharField(max_length=128)),
                ('service_id', models.CharField(max_length=128)),
                ('ips', json_field.fields.JSONField(default=[], help_text='Enter a valid JSON object')),
                ('validate_ip', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='service',
            field=models.ForeignKey(related_name='payments', to='fortumo.Service'),
        ),
    ]
