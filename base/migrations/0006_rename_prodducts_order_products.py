# Generated by Django 5.1.2 on 2024-10-30 03:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_product_likers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='prodducts',
            new_name='products',
        ),
    ]
