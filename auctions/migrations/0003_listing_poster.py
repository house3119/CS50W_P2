# Generated by Django 4.2.4 on 2023-09-14 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='poster',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='usersListings', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
