# Generated by Django 3.2.8 on 2021-10-26 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0020_alter_post_thread'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='name',
        ),
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]