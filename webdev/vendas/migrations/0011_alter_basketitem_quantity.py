# Generated by Django 4.0.4 on 2022-07-04 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0010_alter_basket_markup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basketitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='quantidade'),
        ),
    ]
