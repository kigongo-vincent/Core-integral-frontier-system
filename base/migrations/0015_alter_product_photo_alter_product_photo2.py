# Generated by Django 5.1.2 on 2024-10-31 12:03

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_alter_product_photo_alter_product_photo2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=60, scale=None, size=[1920, 1080], upload_to='static/uploads/products'),
        ),
        migrations.AlterField(
            model_name='product',
            name='photo2',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=60, scale=None, size=[1920, 1080], upload_to='static/uploads/products'),
        ),
    ]
