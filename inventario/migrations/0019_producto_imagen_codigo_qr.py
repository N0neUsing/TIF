# Generated by Django 4.2.6 on 2023-11-27 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0018_cart_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='imagen_codigo_qr',
            field=models.ImageField(blank=True, null=True, upload_to='codigos_qr/'),
        ),
    ]
