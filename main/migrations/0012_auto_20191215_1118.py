# Generated by Django 3.0 on 2019-12-15 11:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20191215_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='note_published',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 15, 11, 18, 27, 361074, tzinfo=utc), verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.URLField(blank=True, default=''),
        ),
    ]