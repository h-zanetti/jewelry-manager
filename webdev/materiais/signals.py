from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

from webdev.financeiro.models import Despesa
from webdev.materiais.models import Entrada

@receiver(pre_save, sender=Entrada)
def gerenciar_entrada(sender, instance, **kwargs):
    material = instance.material
    if instance.pk:
        # Subtrair estoque quando a Entrada é modificada (não foi salva pela primeira vez)
        if instance.alterar_estoque:
            entrada = Entrada.objects.get(pk=instance.pk)
            if entrada.unidades and material.estoque >= entrada.unidades:
                material.estoque -= entrada.unidades
            if entrada.peso and material.peso >= entrada.peso:
                material.peso -= entrada.peso

        if instance.despesa.valor != instance.valor:
            instance.despesa.valor = instance.valor
            instance.despesa.save()
        if instance.despesa.data != instance.data:
            instance.despesa.data = instance.data
            instance.despesa.save()
    else:
        instance.despesa = Despesa.objects.create(
            data=instance.data,
            categoria='Entrada de material',
            valor=instance.valor
        )

    if instance.alterar_estoque:
        # Somar novo estoque
        material.estoque += instance.unidades
        material.peso += instance.peso
        material.save()

@receiver(pre_delete, sender=Entrada)
def deletar_despesa(sender, instance, **kwargs):
    if instance.despesa:
        instance.despesa.delete()