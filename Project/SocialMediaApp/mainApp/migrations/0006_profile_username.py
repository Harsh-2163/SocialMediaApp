# Generated by Django 4.0.1 on 2022-05-29 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0005_profile_coverimg'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='userName',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
