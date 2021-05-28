# Generated by Django 3.1.5 on 2021-05-28 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0016_auto_20210527_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='despesa',
            name='ultimo_pagamento',
            field=models.DateField(blank=True, help_text='Data de encerramento da cobrança de uma despesa repetitiva.', null=True, verbose_name='Último Pagamento'),
        ),
    ]