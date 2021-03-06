# Generated by Django 3.1.5 on 2021-07-05 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0024_auto_20210705_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despesa',
            name='encerrada',
            field=models.BooleanField(blank=True, default=False, help_text='Utilizada para interromper despesas com repetição.', verbose_name='Encerrada'),
        ),
    ]
