# Generated by Django 4.1 on 2023-05-16 14:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_transaction_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'سبد خرید', 'verbose_name_plural': 'سبد خرید ها'},
        ),
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'آیتم سبد خرید', 'verbose_name_plural': 'آیتم های سبد خرید'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'سفارش', 'verbose_name_plural': 'سفارش ها'},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'آیتم سفارش', 'verbose_name_plural': 'آیتم های سفارش'},
        ),
        migrations.AlterField(
            model_name='order',
            name='time_for_pay',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 16, 14, 56, 45, 647287, tzinfo=datetime.timezone.utc), verbose_name='زمال پرداخت'),
        ),
    ]
