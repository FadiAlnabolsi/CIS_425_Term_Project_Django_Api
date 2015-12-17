# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0004_auto_20151215_0237'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrations',
            name='currGpa',
            field=models.CharField(default=2, verbose_name='Cumulative GPA', max_length=4),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='registrations',
            name='collegeStatus',
            field=models.CharField(verbose_name='College Status', max_length=2),
        ),
        migrations.AlterField(
            model_name='registrations',
            name='cumGpa',
            field=models.CharField(verbose_name='Cumulative GPA', max_length=4),
        ),
        migrations.AlterField(
            model_name='registrations',
            name='dob_day',
            field=models.CharField(verbose_name='Date Of Birth - Day', max_length=2),
        ),
        migrations.AlterField(
            model_name='registrations',
            name='dob_month',
            field=models.CharField(verbose_name='Date Of Birth - Month', max_length=2),
        ),
        migrations.AlterField(
            model_name='registrations',
            name='dob_year',
            field=models.CharField(verbose_name='Date Of Birth - Year', max_length=4),
        ),
        migrations.AlterField(
            model_name='registrations',
            name='emailaddress',
            field=models.TextField(verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='registrations',
            name='firstName',
            field=models.CharField(verbose_name='First Name', max_length=50),
        ),
        migrations.AlterField(
            model_name='registrations',
            name='gender',
            field=models.CharField(verbose_name='Gender', max_length=1),
        ),
        migrations.AlterField(
            model_name='registrations',
            name='lastName',
            field=models.CharField(verbose_name='Last Name', max_length=50),
        ),
        migrations.AlterField(
            model_name='registrations',
            name='numCredits',
            field=models.CharField(verbose_name='Number of Credits', max_length=3),
        ),
        migrations.AlterField(
            model_name='registrations',
            name='phoneNumber',
            field=models.CharField(verbose_name='Phone Number', max_length=10),
        ),
        migrations.AlterField(
            model_name='registrations',
            name='studentNumber',
            field=models.CharField(verbose_name='Student Number', max_length=8),
        ),
    ]
