from dateutil.relativedelta import relativedelta
from webdev.financeiro.models import Despesa, Parcela, Receita
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from webdev.vendas.models import Venda
from webdev.materiais.models import Material

@receiver(post_save, sender=Venda)
def criar_receita(sender, instance, created, **kwargs):
    if created:
        receita = Receita.objects.create(categoria='Venda')
        for p in range(instance.parcelas):
            Parcela.objects.create(
                data=instance.data + relativedelta(months=p),
                valor=instance.get_valor_parcela(),
                receita=receita
            )
        instance.receita = receita
        instance.save()
    elif instance.get_valor_parcela() != instance.receita.get_parcelas().first().valor:
        for p in range(instance.parcelas):
            try:
                parcela = instance.receita.get_parcelas().get(data=instance.data + relativedelta(months=p))
                parcela.valor = instance.get_valor_parcela()
                parcela.save()
            except Parcela.DoesNotExist:
                Parcela.objects.create(
                    data=instance.data + relativedelta(months=p),
                    valor=instance.get_valor_parcela(),
                    receita=instance.receita
                )
        instance.receita.save()

@receiver(pre_delete, sender=Venda)
def deletar_receita(sender, instance, **kwargs):
    instance.receita.delete()

@receiver(post_save, sender=Material)
def criar_despesa(sender, instance, created, **kwargs):
    if created:
        despesa = Despesa.objects.create(
            data=instance.entrada,
            categoria='Entrada de Material',
            valor=instance.total_pago
        )
        instance.despesa = despesa
        instance.save()
    else:
        despesa = instance.despesa
        despesa.data = instance.entrada
        despesa.valor = instance.total_pago
        despesa.save()

@receiver(pre_delete, sender=Material)
def deletar_receita(sender, instance, **kwargs):
    instance.despesa.delete()
