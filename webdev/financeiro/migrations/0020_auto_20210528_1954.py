# Generated by Django 3.1.5 on 2021-05-28 22:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0019_auto_20210528_1707'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parcela',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(default=django.utils.timezone.now, verbose_name='Data')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor')),
            ],
        ),
        migrations.RemoveField(
            model_name='receita',
            name='data',
        ),
        migrations.RemoveField(
            model_name='receita',
            name='data_de_encerramento',
        ),
        migrations.RemoveField(
            model_name='receita',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='receita',
            name='valor',
        ),
        migrations.AddField(
            model_name='receita',
            name='parcelas',
            field=models.ManyToManyField(to='financeiro.Parcela', verbose_name='Parcelas'),
        ),
    ]
