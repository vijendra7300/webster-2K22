# Generated by Django 3.1.1 on 2021-04-05 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20210405_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='video_title',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
