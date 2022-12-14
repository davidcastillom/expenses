from django.views.generic import ListView, UpdateView,DetailView, CreateView,DeleteView
from registro.models import tarjetas_credito, movimientos_tc,pagos,gastos
from django.urls import reverse
from django.contrib.auth.models import User

# Create your views here.

# Create your views here.
# [clave,numerotc, nombretc, limite, fecha_vencimiento, dia_corte, dia_pagar_antes, tasa_interes, image, pago_proyectado, pago_minimo, deuda_total ]

class TarjetasCreditoListView(ListView):
    model = tarjetas_credito
    template_name= 'tarjeta_credito/tarjeta_credito_list.html'
    context_object_name='tcs'

    def get_context_data(self, **kwargs):
        context_data = super(TarjetasCreditoListView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data


class TarjetasCreditoUpdateView(UpdateView):
    model = tarjetas_credito
    fields = ['clave', 'numerotc', 'nombretc', 'banco', 'limite', 'fecha_vencimiento', 'dia_corte', 'dia_pagar_antes', 'tasa_interes', 'pago_proyectado','pago_proyectado2','image']
    template_name= 'tarjeta_credito/tarjeta_credito_form.html'
    #template_name= 'gastos/gastos_update.html'
    context_object_name='tc'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super(TarjetasCreditoUpdateView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data

class TarjetasCreditoCreateView(CreateView):
    model = tarjetas_credito
    fields = ['clave', 'numerotc', 'nombretc', 'banco', 'limite', 'fecha_vencimiento', 'dia_corte', 'dia_pagar_antes', 'tasa_interes', 'image']
    template_name= 'tarjeta_credito/tarjeta_credito_form.html'
    #template_name= 'gastos/gastos_update.html'
    context_object_name='tc'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super(TarjetasCreditoCreateView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data

class TarjetasCreditoDetailView(DetailView):
    model = tarjetas_credito     # aqui si vamos a usar el por defecto <app>/<model>_<iwtype>.html
    fields = ['clave', 'numerotc', 'nombretc', 'banco', 'limite', 'fecha_vencimiento', 'dia_corte', 'dia_pagar_antes', 'tasa_interes', 'image']
    template_name= 'tarjeta_credito/tarjeta_credito_detail.html'
    context_object_name='tc'

    def get_context_data(self, **kwargs):
        context_data = super(TarjetasCreditoDetailView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data

class TarjetasCreditoDeleteView(DeleteView):
    model = tarjetas_credito     # aqui si vamos a usar el por defecto <app>/<model>_<iwtype>.html
    success_url = '/tarjeta_credito/tarjeta_credito/'  # luego de borrar va a home
    template_name ='tarjeta_credito/tarjeta_credito_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context_data = super(TarjetasCreditoDeleteView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data



# Create your views here.
class TarjetasCreditosPagoCreateView(CreateView):
    fields = ['forma_de_pago','fecha_pago','monto_pago','folio']
    template_name= 'tarjeta_credito/tarjeta_credito_pagar.html'
    #template_name= 'gastos/gastos_update.html'
    model = pagos
    context_object_name='pagos'

# aqui defino la ruta de retorno al crear el registro en ludar de ponerlo en el modelo
# lo hago aca ya que en el modelo no puedo pasarle el parametro ya que viene de otra
#operacion
    def get_success_url(self, **kwargs):
        context_data = super(TarjetasCreditosPagoCreateView, self).get_context_data(**kwargs)
        v_nrotc = self.kwargs['nrotc']

        return reverse('tarjeta_credito_detail', kwargs={'pk': v_nrotc})

    def form_valid(self, form, **kwargs):
        # aqui debo pagar las cuotas o amortizar pagos en detalle_creditos
        # tambien actualizar el monto en el creditos
        context_data = super(TarjetasCreditosPagoCreateView, self).get_context_data(**kwargs)
        v_numerotc = self.kwargs['nrotc']
        form.instance.usuario = self.request.user
        tc=tarjetas_credito.objects.get(numerotc=v_numerotc)
        field_name = 'clave'
        field_obj=tarjetas_credito._meta.get_field(field_name)
        v_clave= field_obj.value_from_object(tc)
        #form.instance.clave=v_clave
        form.instance.clave=gastos.objects.get(clave=v_clave)
        form.instance.numerotc = v_numerotc # esto tiene que ser en detalle creditos
        # insertar el pago en los movimientos_tc con el monto en negativo
        pago=form.instance.monto_pago
        v_fecha=form.instance.fecha_pago

        #Actualizacion del monto en la abecera de la Tarjeta
        tc=tarjetas_credito.objects.get(numerotc=v_numerotc)
        deuda=tc.deuda_total
        deuda=deuda-pago
        tc.deuda_total=deuda
        tc.save()
        #Creacion del movimiento
        pago=float(pago)*float((-1.00))
        dc=movimientos_tc(numerotc=v_numerotc,
                             tipo_mov='PAGO',
                             fecha=v_fecha,
                             descripcion='Pago',
                             monto=pago,
                             usuario=self.request.user
                             )
        dc.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # en esta variabla context_data coloco el contecto de la clase
        context_data = super(TarjetasCreditosPagoCreateView, self).get_context_data(**kwargs)
        v_numerotc = self.kwargs['nrotc']
        tc=tarjetas_credito.objects.get(numerotc=v_numerotc)

        context_data['Nombre_tc']=tc.nombretc
        context_data['Numero_tc']=tc.numerotc
        context_data['PagoMinimo']=tc.pago_minimo
        #en context_data creo una entrada llamanda Tarjeta y le asigno el parametro con que se llamo la vista
        context_data['PagoProyectado']=tc.pago_proyectado+tc.pago_proyectado2

        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        #retorno el contexto modificado
        return context_data
