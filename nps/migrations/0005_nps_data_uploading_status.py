# Generated by Django 4.2.1 on 2023-06-05 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nps', '0004_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nps_data',
            name='uploading_status',
            field=models.BooleanField(default=False),
        ),
    ]
