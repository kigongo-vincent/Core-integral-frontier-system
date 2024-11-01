# Generated by Django 5.1.2 on 2024-10-30 02:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_product_likers_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='likers',
            field=models.ManyToManyField(blank=True, null=True, related_name='likers', to=settings.AUTH_USER_MODEL),
        ),
    ]
