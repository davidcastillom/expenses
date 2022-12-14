from django.views.generic import ListView, UpdateView,DetailView, CreateView,DeleteView
from registro.models import factura_gastos, tipos, pagos, gastos
#from django.shortcuts import render_to_response, RequestContext
from .forms import FacturaDataImageForm,PagoFacturaForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect



class FacturasListView(ListView):
    model = factura_gastos
    queryset = factura_gastos.objects.order_by('pagada','fecha')
    template_name= 'carga_facturas/carga_facturas_list.html'
    context_object_name='facturas'

    def get_context_data(self, **kwargs):
        context_data = super(FacturasListView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data

class FacturasUpdateView(UpdateView):
    model = factura_gastos
    fields = ['factura','fecha','monto', 'quincena'] #,'pagada','fecha_pago']
    template_name= 'carga_facturas/carga_facturas_form.html'
    #context_object_name='tipos'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super(FacturasUpdateView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data


class FacturasPagarView(UpdateView):
    model = factura_gastos

#    fields = ['factura','fecha','monto','fecha_pago','forma_de_pago','folio', 'pagada']
    fields = ['fecha_pago','forma_de_pago','folio','quincena']
    #readolnly_fields = ['factura','fecha','monto', 'pagada'] #,'pagada','fecha_pago']
    template_name= 'carga_facturas/carga_facturas_pagar.html'
    #context_object_name='tipos'

    def form_valid(self, form):
    # Al ser un pago efectivo, cambio la variable que me indica si la factura fue pagada

        fac=factura_gastos.objects.get(factura=form.instance.factura)
        field_name = 'clave'
        field_obj=factura_gastos._meta.get_field(field_name)
        v_clave= field_obj.value_from_object(fac)
        v_clv=gastos.objects.get(clave=v_clave)

        form.instance.usuario = self.request.user

        form.instance.pagada = '1' # Damos el valor de "r" al campo status
        # aqui vamos a llenar el archivo de pagos
        dc=pagos(fecha_pago=form.instance.fecha_pago,
                             factura=form.instance.factura,
                             forma_de_pago=form.instance.forma_de_pago,
                             monto_pago=form.instance.monto,
                             folio=form.instance.folio,
                             clave=v_clv
                             )
        dc.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super(FacturasPagarView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data



class FacturasCreateView(CreateView):
    model = factura_gastos
    #queryset = tipos.objects.filter(busqueda='Factura')
    fields = ['clave','factura','fecha','monto', 'image'] #,'pagada','fecha_pago']
    template_name= 'carga_facturas/carga_facturas_form.html'
    #template_name= 'tipos/tipos_update.html'
    #context_object_name='tipos'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super(FacturasCreateView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data


class FacturasDetalle(DetailView):
    model = factura_gastos     # aqui si vamos a usar el por defecto <app>/<model>_<iwtype>.html
    fields = ['clave','factura','fecha','monto','image'] #,'pagada','fecha_pago']
    template_name= 'carga_facturas/carga_facturas_detail.html'
    context_object_name='facturas'

    def get_context_data(self, **kwargs):
        context_data = super(FacturasDetalle, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data


class FacturasDetailView(DetailView):
    model = factura_gastos     # aqui si vamos a usar el por defecto <app>/<model>_<iwtype>.html
    #fields = ['id','tipo','descripcion']
    fields = ['clave','factura','fecha','monto'] #,'pagada','fecha_pago']
    template_name= 'carga_facturas/carga_facturas_detail.html'
    context_object_name='facturas'

    def get_context_data(self, **kwargs):
        context_data = super(FacturasDetailView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data


class FacturasDeleteView(DeleteView):
    model = factura_gastos     # aqui si vamos a usar el por defecto <app>/<model>_<iwtype>.html
    success_url = '/carga_facturas/carga_facturas/'  # luego de borrar va a home
    template_name ='carga_facturas/carga_facturas_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context_data = super(FacturasDeleteView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data
