# Generated by Django 3.2.8 on 2022-01-08 15:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0011_auto_20211006_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='data_criacao',
            field=models.DateField(blank=True, default=django.utils.timezone.localdate, null=True, verbose_name='Data de Criação'),
        ),
    ]
