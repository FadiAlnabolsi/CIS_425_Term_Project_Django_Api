# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0005_auto_20151217_0414'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrations',
            name='winner',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='registrations',
            name='currGpa',
            field=models.CharField(max_length=4, verbose_name='Semester GPA'),
        ),
    ]
