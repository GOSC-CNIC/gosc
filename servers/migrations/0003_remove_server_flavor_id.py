# Generated by Django 2.2.16 on 2020-09-25 03:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0002_auto_20200922_0253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='flavor_id',
        ),
    ]
