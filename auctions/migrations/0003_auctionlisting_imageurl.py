# Generated by Django 3.2.4 on 2021-06-29 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctioncomment_auctionlisting_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='imageurl',
            field=models.CharField(default='', max_length=250),
        ),
    ]
