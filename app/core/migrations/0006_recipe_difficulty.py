# Generated by Django 2.1.15 on 2021-07-23 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210723_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='difficulty',
            field=models.CharField(default='Unkown', max_length=255),
        ),
    ]
