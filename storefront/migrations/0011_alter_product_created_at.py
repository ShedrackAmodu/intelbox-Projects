# Generated by Django 4.2.13 on 2024-06-08 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storefront', '0010_alter_product_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]