# Generated by Django 5.0.4 on 2024-05-11 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_delete_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='quantity',
        ),
    ]
