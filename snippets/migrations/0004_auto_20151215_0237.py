# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0003_auto_20151215_0129'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registrations',
            options={'verbose_name_plural': 'Registrations', 'verbose_name': 'Registration'},
        ),
        migrations.RenameField(
            model_name='scholarshipadmin',
            old_name='isAdmin',
            new_name='Admin',
        ),
    ]
