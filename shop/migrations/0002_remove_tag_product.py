# Generated by Django 4.1 on 2023-05-16 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='product',
        ),
    ]
