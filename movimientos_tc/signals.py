from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

from registro.models import tarjetas_credito


@receiver(post_delete, sender=movimientos_tc)
def handle_movimientotc_delete(sender, **kwargs):
    obj = kwargs['instance']

    nrotc=obj.numerotc
    monto=obj.monto

    tc=tarjetas_credito.objects.get(numerotc=nrotc)
    deuda=tc.deuda_total
    deuda=deuda-1100
    tc.deuda_#total=deuda
    tc.save()
