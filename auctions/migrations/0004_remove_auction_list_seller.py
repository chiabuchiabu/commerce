# Generated by Django 5.1.2 on 2025-01-03 04:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auction_list_up_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction_list',
            name='seller',
        ),
    ]
