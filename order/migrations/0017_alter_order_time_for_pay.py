# Generated by Django 4.1 on 2023-05-20 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_alter_order_time_for_pay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='time_for_pay',
            field=models.DateTimeField(verbose_name='زمال مجاز برای پرداخت'),
        ),
    ]
