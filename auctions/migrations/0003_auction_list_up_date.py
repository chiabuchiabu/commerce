# Generated by Django 5.1.2 on 2025-01-02 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_list',
            name='up_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
