# Generated by Django 5.1.7 on 2025-03-26 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_events_event_date_events_poster_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='whatsapp_group_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
