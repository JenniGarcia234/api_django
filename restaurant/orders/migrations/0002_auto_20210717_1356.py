# Generated by Django 3.2.5 on 2021-07-17 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='activate',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='activate',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
