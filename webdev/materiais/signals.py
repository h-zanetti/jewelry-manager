from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

from webdev.financeiro.models import Despesa
from webdev.materiais.models import Entrada

@receiver(pre_save, sender=Entrada)
def gerenciar_entrada(sender, instance, **kwargs):
    material = instance.material
    try:
        # Verifica se entrada existe
        entrada = Entrada.objects.get(pk=instance.pk)
        # Verifica se altera o estoque
        if entrada.alterar_estoque:
            if entrada.unidades and material.estoque >= entrada.unidades:
                material.estoque -= entrada.unidades
            if entrada.peso and material.peso >= entrada.peso:
                material.peso -= entrada.peso
        #  Verifica se altera a despesa
        if entrada.despesa.valor != instance.valor:
            instance.despesa.valor = instance.valor
            instance.despesa.save()
        if entrada.despesa.data != instance.data:
            instance.despesa.data = instance.data
            instance.despesa.save()
    except Entrada.DoesNotExist:
        instance.despesa = Despesa.objects.create(
            data=instance.data,
            categoria='Entrada de material',
            valor=instance.valor
        )

    # Soma estoque ao criar entrada
    if instance.alterar_estoque:
        if instance.unidades:
            material.estoque += instance.unidades
            material.save()
        if instance.peso:
            material.peso += instance.peso
            material.save()

@receiver(pre_delete, sender=Entrada)
def deletar_despesa(sender, instance, **kwargs):
    if instance.despesa:
        instance.despesa.delete()