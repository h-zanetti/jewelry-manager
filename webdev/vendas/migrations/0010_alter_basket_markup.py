# Generated by Django 4.0.4 on 2022-07-04 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0009_alter_markup_value_alter_venda_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='markup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendas.markup', verbose_name='mark up'),
        ),
    ]
