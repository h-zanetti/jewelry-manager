from django.contrib import messages
from webdev.financeiro.models import Despesa
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from webdev.materiais.models import Entrada

@receiver(pre_save, sender=Entrada)
def alterar_estoque(sender, instance, **kwargs):
    # Subtrair peso e unidades quando modificado
    material = instance.material
    if instance.id != None:
        if material.estoque:
            material.estoque -= instance.unidades
        if material.peso:
            material.peso -= instance.peso
    # Adicionar peso e unidades
    material.estoque += instance.unidades
    if material.peso is None:
        material.peso = instance.peso
        material.unidade_de_medida = instance.unidade_de_medida
    else:
        material.peso += instance.peso
    material.save()

@receiver(post_save, sender=Entrada)
def criar_despesa(sender, instance, created, **kwargs):
    if created:
        despesa = Despesa.objects.create(
            data=instance.data,
            categoria='Entrada de material',
            valor=instance.valor
        )
        instance.despesa = despesa
        instance.save()
    else:
        if instance.valor != instance.despesa.valor:
            instance.despesa.valor = instance.valor
            instance.despesa.save()
        if instance.data != instance.despesa.data:
            instance.despesa.data = instance.data
            instance.despesa.save()

@receiver(pre_delete, sender=Entrada)
def deletar_despesa(sender, instance, **kwargs):
    if instance.despesa:
        instance.despesa.delete()