from django.db import models
from django.utils.translation import gettext_lazy as _

class Fornecimento(models.Model):
    nome = models.CharField(_("Fornecimento"), max_length=150, help_text="Serviços ou produtos fornecidos.")
    qualidade = models.IntegerField(_("Qualidade"), default=0)

    def __str__(self):
        return f"{self.nome} ({self.qualidade})"


class Email(models.Model):
    email = models.EmailField(_("Endereço de Email"), unique=True)

    def __str__(self):
        return f"{self.email}"


class Telefone(models.Model):
    telefone = models.CharField(_('Telefone'), max_length=15, unique=True)

    def __str__(self):
        return f'{self.telefone}'


class Local(models.Model):
    pais = models.CharField(_('País'), max_length=50, blank=True, null=True)
    estado = models.CharField(_('Estado'), max_length=2, blank=True, null=True)
    cidade = models.CharField(_('Cidade'), max_length=50, blank=True, null=True)
    bairro = models.CharField(_('Bairro'), max_length=100, blank=True, null=True)
    endereco = models.CharField(_('Endereço'), max_length=100, blank=True, null=True)
    cep = models.CharField(_('CEP'), max_length=15, blank=True, null=True)

    def __str__(self):
        if self.bairro:
            local = f'{self.bairro}, {self.cidade}'
        else:
            local = f"{self.cidade}, {self.estado}"
        return local

class DadosBancarios(models.Model):
    TIPO_DE_TRANSACAO_CHOICES = (
        ('cc', 'Conta Corrente'),
        ('px', 'Pix'),
    )
    tipo_de_transacao = models.CharField(_("Tipo de Transação"), max_length=2, choices=TIPO_DE_TRANSACAO_CHOICES)
    banco = models.CharField(_('Banco'), max_length=100, null=True, blank=True)
    agencia = models.CharField(_('Agência'), max_length=10, null=True, blank=True)
    numero = models.CharField(_('Número da Conta'), max_length=50, help_text='Ou chave do Pix')

class Fornecedor(models.Model):
    foto = models.ImageField(_('Foto do Fornecedor'), upload_to='fornecedores', default='default.jpg', blank=True, null=True)
    nome = models.CharField(_('Nome'), max_length=150)
    emails = models.ManyToManyField(Email, verbose_name=_("Endereços de Email"), blank=True)
    telefones = models.ManyToManyField(Telefone, verbose_name=_('Telefones'), blank=True)
    localizacoes = models.ManyToManyField(Local, verbose_name=_('Localizações'), blank=True)
    fornecimento = models.ManyToManyField(Fornecimento, verbose_name=_('Fornecimentos'), blank=True)
    documento = models.CharField(_('Documento'), max_length=20, help_text='Digite o CNPJ ou IE do fornecedor.', blank=True, null=True)
    dados_bancarios = models.ManyToManyField(DadosBancarios, verbose_name=_('Dados Bancários'), blank=True)

    def __str__(self):
        return self.nome
