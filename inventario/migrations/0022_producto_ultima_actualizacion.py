# Generated by Django 4.2.6 on 2024-03-26 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0021_alter_producto_codigo_barra'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='ultima_actualizacion',
            field=models.DateTimeField(auto_now=True),
        ),
    ]