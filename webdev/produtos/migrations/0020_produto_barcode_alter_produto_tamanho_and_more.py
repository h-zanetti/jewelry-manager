# Generated by Django 4.0.4 on 2022-05-17 18:33

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0019_remove_produto_materiais_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='barcode',
            field=models.ImageField(blank=True, null=True, upload_to='produtos/barcode/', verbose_name='código de barras'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='tamanho',
            field=models.IntegerField(blank=True, null=True, verbose_name='tamanho'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='unidades',
            field=models.IntegerField(default=0, verbose_name='unidades em estoque'),
        ),
    ]