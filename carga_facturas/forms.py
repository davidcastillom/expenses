from django import forms
from registro.models import factura_gastos
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime #for checking renewal date range.


class FacturaDataImageForm(forms.ModelForm):



    class Meta:
        model=factura_gastos
        fields = '__all__'  # ['camp1','campo2']


class PagoFacturaForm(forms.Form):

    TRANSFERENCIA='Transferencia'
    PAGO_EN_LINEA='Pago en Linea'
    PAGO_EN_TIENDA='Pago en Tienda'
    PAGO_EN_FARMACIA='Pago en Farmacia'

    valores_busqueda=((TRANSFERENCIA,'Transferencia'),
        (PAGO_EN_LINEA,'Pago en Linea'),
        (PAGO_EN_TIENDA,'Pago en Tienda'),
        (PAGO_EN_FARMACIA,'Pago en Farmacia'))

    factura = forms.CharField(max_length=15, disabled=True)
    fecha= forms.DateField(disabled=True)
    monto = forms.DecimalField(max_digits=12, decimal_places=2,disabled=True)

    fecha_pago = forms.DateField()
    forma_de_pago=forms.CharField(max_length=20)
    folio=forms.CharField(max_length=15)
    pagada = forms.CharField(max_length=1)
