# Generated by Django 4.2.13 on 2024-07-06 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_reserved',
            field=models.BooleanField(default=False),
        ),
    ]
