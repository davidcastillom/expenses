from django.contrib import admin
from registro.models import gastos, tipos

# Register your models here.

def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'clave':
            kwargs['queryset'] = gastos.objects.filter(tipo=='B').order_by('tipo')
        return super(ConsumerAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
