# Generated by Django 3.1.5 on 2021-05-08 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0006_auto_20210507_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialdoproduto',
            name='unidades',
            field=models.IntegerField(default=1, verbose_name='Unidades Utilizadas'),
        ),
    ]
