from django.db import models
from django.db.models.aggregates import Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Receita(models.Model):
    categoria = models.CharField(_("Categoria"), max_length=150)
    
    class Meta:
        get_latest_by = "data"

    def __str__(self):
        return self.categoria

    @classmethod
    def get_tipo_de_transacao(cls):
        return 'Receita'

    def get_parcelas(self):
        return Parcela.objects.filter(receita=self.id)

    def get_valor_total(self):
        return float(self.get_parcelas().aggregate(Sum('valor'))['valor__sum'])


class Parcela(models.Model):
    data = models.DateField(_("Data"), default=timezone.now)
    valor = models.DecimalField(_("Valor"), max_digits=8, decimal_places=2)
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, verbose_name=_("Receita"))

    def __str__(self):
        return f"{self.data} {self.valor}"

class Despesa(models.Model):
    data = models.DateField(_("Data"), default=timezone.now)
    categoria = models.CharField(_("Categoria"), max_length=150)
    valor = models.DecimalField(_("Valor"), max_digits=8, decimal_places=2)
    REPETIR_CHOICES = (
        ('', 'Nunca'),
        ('m', 'Mensalmente'),
        ('a', 'Anualmente'),
    )
    repetir = models.CharField(_("Repetir"), max_length=1, choices=REPETIR_CHOICES, default='')
    is_active = models.BooleanField(_("Despesa ativa"), default=True, help_text='Variável usada para interromper despesas com repetição.')
    data_de_encerramento = models.DateField(_("Data de Encerramento"), null=True, blank=True, help_text='Data de encerramento da cobrança de uma despesa repetitiva.')

    class Meta:
        get_latest_by = "data"

    def __str__(self):
        return self.categoria

    @classmethod
    def get_tipo_de_transacao(cls):
        return 'Despesa'