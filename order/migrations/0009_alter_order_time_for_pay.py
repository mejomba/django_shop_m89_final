# Generated by Django 4.1 on 2023-05-18 19:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_alter_order_time_for_pay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='time_for_pay',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 18, 19, 38, 31, 373635, tzinfo=datetime.timezone.utc), verbose_name='زمال پرداخت'),
        ),
    ]