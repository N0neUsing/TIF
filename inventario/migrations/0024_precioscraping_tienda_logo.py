# Generated by Django 4.2.6 on 2024-04-13 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0023_remove_producto_tiene_iva_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='precioscraping',
            name='tienda_logo',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
