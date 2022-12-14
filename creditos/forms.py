from django.forms import ModelForm
#from betterforms.multiform import MultiModelForm
from registro.models import creditos, detalle_creditos

class CreditosModelForm(ModelForm):
    class Meta:
        model = creditos
        fields = '__all__'

class DetalleModelForm(ModelForm):
    class Meta:
        model = detalle_creditos
        fields = ['numero_cuota','mes','ano','pagada', 'monto_cuota', 'intereses','iva_intereses','amortiza', 'capital']


"""
class UnionPersonaModelForm(MultimodelForm):
    form_classes = {
        'creditos':CreditosModelForm,
        'detalle_creditos':DEtalleModelForm,
    }
"""
