# Generated by Django 3.2.8 on 2021-10-30 13:33

from django.db import migrations, models
import pathlib


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0022_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=pathlib.PurePosixPath('/home/mateusz/Pulpit/forum/ForumProject/media')),
        ),
    ]
