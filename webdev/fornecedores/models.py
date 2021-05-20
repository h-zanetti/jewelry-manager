from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Fornecimento(models.Model):
    nome = models.CharField(_("Fornecimento"), max_length=150, help_text="Serviços ou produtos fornecidos.")
    qualidade = models.IntegerField(_("Qualidade"), default=0)

    def __str__(self):
        return f"{self.nome} ({self.qualidade})"

class Fornecedor(models.Model):
    nome = models.CharField(_('Nome Completo'), max_length=150)
    fornecimento = models.ManyToManyField(Fornecimento, verbose_name=_('Fornecimentos'), blank=True)

    def __str__(self):
        return self.nome

    def get_servicos(self):
        return Servico.objects.filter(fornecedor=self.id)

    def get_emails(self):
        return Email.objects.filter(fornecedor=self.id)

    def get_telefones(self):
        return Telefone.objects.filter(fornecedor=self.id)

    def get_documentos(self):
        return Documento.objects.filter(fornecedor=self.id)

    def get_dados_bancarios(self):
        return DadosBancarios.objects.filter(fornecedor=self.id)

    def get_localizacoes(self):
        return Local.objects.filter(fornecedor=self.id)

    def get_fornecimentos(self):
        return Fornecimento.objects.filter(fornecedor=self.id).order_by('-qualidade')


class Email(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, models.CASCADE, verbose_name=_("Fornecedor"))
    email = models.EmailField(_("Endereço de Email"), unique=True)

    def __str__(self):
        return f"{self.email}"


class Telefone(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, models.CASCADE, verbose_name=_("Fornecedor"))
    telefone = models.CharField(_('Telefone'), max_length=15, unique=True)

    def __str__(self):
        return f'{self.telefone}'


class Local(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, models.CASCADE, verbose_name=_("Fornecedor"))
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
    fornecedor = models.ForeignKey(Fornecedor, models.CASCADE, verbose_name=_("Fornecedor"))
    TIPO_DE_TRANSACAO_CHOICES = (
        ('', 'Tipo de Transação'),
        ('cc', 'Conta Corrente'),
        ('px', 'Pix'),
    )
    tipo_de_transacao = models.CharField(_("Tipo de Transação"), max_length=2, choices=TIPO_DE_TRANSACAO_CHOICES)
    banco = models.CharField(_('Banco'), max_length=100, null=True, blank=True)
    agencia = models.CharField(_('Agência'), max_length=10, null=True, blank=True)
    numero = models.CharField(_('Número da Conta'), max_length=50, help_text='Ou chave Pix')

class Documento(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, models.CASCADE, verbose_name=_("Fornecedor"))
    nome = models.CharField(_('Tipo de Documento'), max_length=20, help_text='Exemplos: CNPJ, IE')
    numero = models.CharField(_('Número'), max_length=20)

class Servico(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, verbose_name=_("Fornecedor"))
    nome = models.CharField(_('Serviço'), max_length=150)
    data = models.DateField(_("Data"), default=timezone.now)
    qualidade = models.IntegerField(_("Qualidade"), default=0)
    total_pago = models.DecimalField(_("Total Pago"), max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.fornecedor} - {self.nome} ({self.qualidade})"
