# Generated by Django 3.2.8 on 2021-10-31 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiais', '0020_auto_20211020_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='altura',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='altura'),
        ),
        migrations.AlterField(
            model_name='material',
            name='comprimento',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='comprimento'),
        ),
        migrations.AlterField(
            model_name='material',
            name='largura',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='largura'),
        ),
    ]