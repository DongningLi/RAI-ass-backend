# Generated by Django 4.1 on 2024-06-13 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ColsTypes',
        ),
        migrations.DeleteModel(
            name='FileContent',
        ),
    ]
