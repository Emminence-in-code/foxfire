# Generated by Django 5.1.1 on 2024-10-09 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0003_customuser_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='country',
            field=models.CharField(blank=True, default='Nigeria', max_length=200, null=True),
        ),
    ]
