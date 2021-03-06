# Generated by Django 3.1.5 on 2021-05-03 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fornecedores', '0007_auto_20210501_2030'),
    ]

    operations = [
        migrations.CreateModel(
            name='DadosBancarios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_de_transacao', models.CharField(choices=[('cc', 'Conta Corrente'), ('px', 'Pix')], max_length=2, verbose_name='Tipo de Pagamento')),
                ('bank', models.CharField(blank=True, max_length=100, null=True, verbose_name='Banco')),
                ('branch', models.CharField(blank=True, max_length=10, null=True, verbose_name='Agência')),
                ('number', models.CharField(help_text='Ou chave do Pix', max_length=50, verbose_name='Número da Conta')),
            ],
        ),
        migrations.AddField(
            model_name='fornecedor',
            name='dados_bancarios',
            field=models.ManyToManyField(blank=True, to='fornecedores.DadosBancarios', verbose_name='Dados Bancários'),
        ),
    ]
