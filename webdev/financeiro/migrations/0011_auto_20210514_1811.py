# Generated by Django 3.1.5 on 2021-05-14 21:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0010_auto_20210514_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venda',
            name='data',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Data'),
        ),
    ]
