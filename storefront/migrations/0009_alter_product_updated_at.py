# Generated by Django 4.2.13 on 2024-06-08 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storefront', '0008_alter_product_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(),
        ),
    ]