# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-06-18 11:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0020_auto_20180126_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancerecord',
            name='attend_time',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='exam',
            name='exam_time',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='examrecord',
            name='exam_time',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='examrecord',
            name='student_degree',
            field=models.FloatField(db_index=True),
        ),
    ]
