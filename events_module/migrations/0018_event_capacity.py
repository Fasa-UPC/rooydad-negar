# Generated by Django 5.0.2 on 2024-02-26 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_module', '0017_alter_userdescount_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='capacity',
            field=models.IntegerField(default=0, null=True, verbose_name='ظرفیت دوره'),
        ),
    ]
