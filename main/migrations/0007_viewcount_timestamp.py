# Generated by Django 5.2.3 on 2025-07-01 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_quote_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewcount',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default='2024-01-01T00:00:00'),
            preserve_default=False,
        ),
    ]
