# Generated by Django 2.1.5 on 2019-04-18 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0004_notificaciones'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='tipo',
            field=models.CharField(choices=[('1', 'Comestibles'), ('2', 'Muebles'), ('3', 'Tecnologicos'), ('4', 'Otros')], max_length=20),
        ),
    ]
