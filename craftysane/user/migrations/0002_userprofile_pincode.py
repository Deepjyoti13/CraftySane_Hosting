# Generated by Django 3.1.1 on 2020-12-29 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='PINcode',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
