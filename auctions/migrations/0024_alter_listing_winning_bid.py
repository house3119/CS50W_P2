# Generated by Django 4.2.4 on 2023-09-14 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0023_listing_winning_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='winning_bid',
            field=models.IntegerField(null=True),
        ),
    ]
