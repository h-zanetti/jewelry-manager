# Generated by Django 3.1.5 on 2021-04-28 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0002_auto_20210428_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='categorias',
            field=models.ManyToManyField(blank=True, to='produtos.Categoria', verbose_name='Categorias'),
        ),
    ]
