# Generated by Django 3.1.5 on 2021-06-16 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0021_auto_20210530_1434'),
        ('fornecedores', '0020_auto_20210616_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servico',
            name='despesa',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='financeiro.despesa', verbose_name='Despesa'),
        ),
    ]
