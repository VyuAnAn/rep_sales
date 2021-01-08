# Generated by Django 3.1.4 on 2021-01-08 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('records', '0008_auto_20210108_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleslog',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_profiles', related_query_name='customer_profile', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель'),
        ),
        migrations.AddField(
            model_name='saleslog',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seller_profiles', related_query_name='seller_profile', to=settings.AUTH_USER_MODEL, verbose_name='Продавец'),
        ),
    ]