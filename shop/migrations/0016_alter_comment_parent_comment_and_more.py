# Generated by Django 4.1 on 2023-05-19 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_alter_product_magic_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.comment'),
        ),
        migrations.AlterField(
            model_name='product',
            name='magic_sale',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.magicsale', verbose_name='حراج شگفت انگیز'),
        ),
    ]
