# Generated by Django 5.1.1 on 2024-09-25 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_survey_upload_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawrequest',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
