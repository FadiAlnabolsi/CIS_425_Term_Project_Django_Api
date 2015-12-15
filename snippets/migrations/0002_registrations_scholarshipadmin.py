# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('snippets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registrations',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('firstName', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
                ('studentNumber', models.CharField(max_length=8)),
                ('emailaddress', models.TextField()),
                ('phoneNumber', models.CharField(max_length=10)),
                ('dob_day', models.CharField(max_length=2)),
                ('dob_month', models.CharField(max_length=2)),
                ('dob_year', models.CharField(max_length=4)),
                ('registration_day', models.CharField(max_length=2)),
                ('registration_month', models.CharField(max_length=2)),
                ('registration_year', models.CharField(max_length=4)),
                ('gender', models.CharField(max_length=1)),
                ('collegeStatus', models.CharField(max_length=2)),
                ('cumGpa', models.CharField(max_length=3)),
                ('numCredits', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='ScholarshipAdmin',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('isAdmin', models.BooleanField(default=False)),
                ('user', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
