# Generated by Django 3.1.4 on 2021-01-08 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0007_auto_20210108_1335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saleslog',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='saleslog',
            name='seller',
        ),
    ]
