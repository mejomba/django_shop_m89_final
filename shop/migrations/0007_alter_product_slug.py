# Generated by Django 4.1 on 2023-05-16 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_remove_tag_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, verbose_name='نام منحصر به فرد'),
        ),
    ]
