# Generated by Django 4.0.1 on 2022-02-09 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0015_alter_produto_data_criacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='cor',
            field=models.CharField(blank=True, max_length=75, null=True, verbose_name='Cor'),
        ),
    ]
