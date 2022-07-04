from django.dispatch import receiver
from webdev.vendas.models import Venda
from webdev.fornecedores.models import Servico
from dateutil.relativedelta import relativedelta
from webdev.financeiro.models import Despesa, Parcela, Receita
from django.db.models.signals import post_save, pre_delete, post_delete

# Vendas
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

@receiver(post_delete, sender=Venda)
def deletar_receita(sender, instance, **kwargs):
    if instance.receita != None:
        instance.receita.delete()

# Serviços
@receiver(post_save, sender=Servico)
def criar_despesa_de_servico(sender, instance, created, **kwargs):
    if created:
        despesa = Despesa.objects.create(
            data=instance.data,
            categoria='Serviço contratado',
            valor=instance.valor
        )
        instance.despesa = despesa
        instance.save()
    else:
        if instance.despesa != None:
            despesa = instance.despesa
            despesa.data = instance.data
            despesa.valor = instance.valor
            despesa.save()

@receiver(pre_delete, sender=Servico)
def deletar_despesa_de_servico(sender, instance, **kwargs):
    if instance.despesa != None:
        instance.despesa.delete()
