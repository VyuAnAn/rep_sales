# Generated by Django 3.1.4 on 2021-01-07 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(max_length=16, null=True, verbose_name='Номер телефона'),
        ),
    ]
