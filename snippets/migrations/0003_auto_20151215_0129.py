# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0002_registrations_scholarshipadmin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrations',
            name='cumGpa',
            field=models.CharField(max_length=4),
        ),
    ]
