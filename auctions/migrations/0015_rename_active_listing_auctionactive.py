# Generated by Django 4.2.4 on 2023-09-14 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_listing_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='active',
            new_name='auctionActive',
        ),
    ]