# Generated by Django 4.0.1 on 2022-02-21 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiais', '0022_alter_material_peso'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='valor',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, verbose_name='valor'),
        ),
    ]
