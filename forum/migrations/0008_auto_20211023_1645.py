# Generated by Django 3.2.8 on 2021-10-23 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_alter_forumgroup_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='forumgroup',
            name='permissions',
        ),
        migrations.AddField(
            model_name='forumgroup',
            name='permissions',
            field=models.ManyToManyField(to='forum.Permission'),
        ),
    ]
