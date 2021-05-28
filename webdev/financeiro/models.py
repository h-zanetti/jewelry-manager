from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Receita(models.Model):
    data = models.DateField(_("Data"), default=timezone.now)
    categoria = models.CharField(_("Categoria"), max_length=150)
    valor = models.DecimalField(_("Valor"), max_digits=8, decimal_places=2)

    class Meta:
        get_latest_by = "data"

    def __str__(self):
        return self.categoria


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

