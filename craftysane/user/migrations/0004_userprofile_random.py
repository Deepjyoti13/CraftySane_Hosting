# Generated by Django 3.1.4 on 2021-02-03 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20201230_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='random',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
