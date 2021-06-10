# Generated by Django 3.1.5 on 2021-05-28 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0017_despesa_ultimo_pagamento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='despesa',
            name='ultimo_pagamento',
        ),
        migrations.AddField(
            model_name='despesa',
            name='data_de_encerramento',
            field=models.DateField(blank=True, help_text='Data de encerramento da cobrança de uma despesa repetitiva.', null=True, verbose_name='Data de Encerramento'),
        ),
        migrations.AlterField(
            model_name='despesa',
            name='repetir',
            field=models.CharField(choices=[('', 'Nunca'), ('m', 'Mensalmente'), ('a', 'Anualmente')], default='', max_length=1, verbose_name='Repetir'),
        ),
    ]
