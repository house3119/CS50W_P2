# Generated by Django 4.2.4 on 2023-09-14 13:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_listing_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]