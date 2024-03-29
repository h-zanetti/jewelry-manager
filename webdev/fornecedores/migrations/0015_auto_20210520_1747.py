# Generated by Django 3.1.5 on 2021-05-20 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fornecedores', '0014_remove_fornecedor_foto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fornecedor',
            name='dados_bancarios',
        ),
        migrations.RemoveField(
            model_name='fornecedor',
            name='documentos',
        ),
        migrations.RemoveField(
            model_name='fornecedor',
            name='emails',
        ),
        migrations.RemoveField(
            model_name='fornecedor',
            name='localizacoes',
        ),
        migrations.RemoveField(
            model_name='fornecedor',
            name='telefones',
        ),
        migrations.AddField(
            model_name='dadosbancarios',
            name='fornecedor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='fornecedores.fornecedor', verbose_name='Fornecedor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='email',
            name='fornecedor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='fornecedores.fornecedor', verbose_name='Fornecedor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='local',
            name='fornecedor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='fornecedores.fornecedor', verbose_name='Fornecedor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='telefone',
            name='fornecedor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='fornecedores.fornecedor', verbose_name='Fornecedor'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dadosbancarios',
            name='numero',
            field=models.CharField(help_text='Ou chave Pix', max_length=50, verbose_name='Número da Conta'),
        ),
        migrations.AlterField(
            model_name='documento',
            name='nome',
            field=models.CharField(help_text='Exemplos: CNPJ, IE', max_length=20, verbose_name='Tipo de Documento'),
        ),
        migrations.AlterField(
            model_name='fornecedor',
            name='nome',
            field=models.CharField(max_length=150, verbose_name='Nome Completo'),
        ),
    ]
