# Generated by Django 4.2.4 on 2023-09-14 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_rename_active_listing_auctionactive'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='auctionActive',
            new_name='active',
        ),
    ]
