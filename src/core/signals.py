from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Candidato, Empresa


def remove_related(instance):
    if isinstance(instance, (Candidato, Empresa,)):
        instance.user.delete()
        instance.endereco.delete()
        instance.contato.delete()


@receiver(post_delete, sender=Candidato)
def post_delete_candidato(instance, **kwargs):
    remove_related(instance)


@receiver(post_delete, sender=Empresa)
def post_delete_empresa(instance, **kwargs):
    remove_related(instance)
