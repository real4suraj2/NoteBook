# Generated by Django 3.0 on 2019-12-15 16:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20191215_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='note_published',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 15, 16, 13, 19, 443812, tzinfo=utc), verbose_name='date published'),
        ),
    ]