# Generated by Django 3.0.5 on 2020-05-28 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20200528_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
