# Generated by Django 3.0 on 2019-12-13 16:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20191213_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='note_published',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 13, 16, 55, 20, 617761, tzinfo=utc), verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='notecategory',
            name='category_image',
            field=models.CharField(choices=[('classwork', 'Class Work!'), ('projectwork', 'Project Work!'), ('labwork', 'Laboratory Work'), ('explore', 'Explore the world!')], default='classwork', max_length=50),
        ),
    ]
