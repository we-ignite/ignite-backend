# Generated by Django 5.1.7 on 2025-03-27 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_entries_customer_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='payment',
        ),
    ]
