# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fortumo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('pin', models.CharField(max_length=16, unique=True)),
                ('used', models.BooleanField(default=False)),
                ('message', models.OneToOneField(to='fortumo.Message')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('secret', models.CharField(max_length=128)),
                ('service_id', models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='service',
            field=models.ForeignKey(to='fortumo.Service', related_name='payments'),
        ),
    ]
