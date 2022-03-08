# Generated by Django 4.0.1 on 2022-03-03 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiais', '0023_material_valor'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='alterar_estoque',
            field=models.BooleanField(default=True, help_text='Define se esta entrada deve ser adicionada ao estoque.', verbose_name='altera estoque'),
        ),
    ]
