# Generated by Django 3.0 on 2019-12-13 16:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20191213_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='note_published',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 13, 16, 25, 37, 588496, tzinfo=utc), verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='noteseries',
            name='series_image',
            field=models.TextField(default='https://source.unsplash.com/random/400x350'),
        ),
    ]
