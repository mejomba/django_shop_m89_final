# Generated by Django 4.1 on 2023-05-28 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_user_profile_image_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(default=0, max_length=11, unique=True, verbose_name='شماره تلفن'),
            preserve_default=False,
        ),
    ]