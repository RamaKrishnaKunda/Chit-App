# Generated by Django 2.0.5 on 2018-06-30 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chit_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lifted',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
