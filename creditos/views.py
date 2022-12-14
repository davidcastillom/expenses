from django.views.generic import ListView, UpdateView,DetailView, CreateView,DeleteView
from registro.models import creditos, detalle_creditos,entidad, pagos, gastos
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from datetime import date, time, datetime
from decimal import Decimal
from django.urls import reverse
from .forms import CreditosModelForm,DetalleModelForm   #UnionPersonaModelForm
from django.contrib.auth.models import User

#['cod_entidad','cod_credito','articulo','costo_original','tasa_interes','plazo_meses','costo_credito','image','pagada']

class CreditosListView(ListView):
    model = creditos
    queryset = creditos.objects.order_by('pagada')
    template_name= 'creditos/creditos_list.html'
    context_object_name='creditos'


    def get_context_data(self, **kwargs):
        context_data = super(CreditosListView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data


class CreditosPagoCreateView(CreateView):
    fields = ['forma_de_pago','fecha_pago','monto_pago','folio']
    template_name= 'creditos/creditos_pagar.html'
    #template_name= 'gastos/gastos_update.html'
    model = pagos
    context_object_name='pagos'

# aqui defino la ruta de retorno al crear el registro en ludar de ponerlo en el modelo
# lo hago aca ya que en el modelo no puedo pasarle el parametro ya que viene de otra
#operacion
    def get_success_url(self, **kwargs):
        context_data = super(CreditosPagoCreateView, self).get_context_data(**kwargs)
        v_cod_credito = self.kwargs['codigo']
        return reverse('creditos_detail', kwargs={'codigo': v_cod_credito})

    def form_valid(self, form, **kwargs):
        # aqui debo pagar las cuotas o amortizar pagos en detalle_creditos
        # tambien actualizar el monto en el creditos
        context_data = super(CreditosPagoCreateView, self).get_context_data(**kwargs)
        v_cod_credito = self.kwargs['codigo']

        form.instance.usuario = self.request.user

        cr=creditos.objects.get(cod_credito=v_cod_credito)
        field_name = 'cod_entidad'
        field_obj=creditos._meta.get_field(field_name)
        v_entidad= field_obj.value_from_object(cr)

        entid=entidad.objects.get(cod_entidad=v_entidad)
        field_name = 'clave'
        field_obj=entidad._meta.get_field(field_name)
        v_clave= field_obj.value_from_object(entid)

        form.instance.clave=gastos.objects.get(clave=v_clave)
        #form.instance.clave=v_clave


        form.instance.cod_credito = v_cod_credito # esto tiene que ser en detalle creditos
        # Actualizar el detalle_creditos
        detalle = detalle_creditos.objects.filter(cod_credito=v_cod_credito).filter(pagada='0').order_by('numero_cuota')
        pago=form.instance.monto_pago
        for det in detalle:
            if pago!=0:
                a_pagar = det.monto_cuota-det.abono_a_cuota

                id=det.id_credito
                dc=detalle_creditos.objects.get(id_credito=id)

                dc.usuario = self.request.user

                if a_pagar<=pago:
                    dc.abono_a_cuota=dc.abono_a_cuota+a_pagar
                    if dc.abono_a_cuota==dc.monto_cuota:
                        dc.pagada='1'
                else:
                    a_pagar=pago
                    dc.abono_a_cuota=dc.abono_a_cuota+a_pagar
                pago=pago-a_pagar
                dc.save()
        detalle = detalle_creditos.objects.filter(cod_credito=v_cod_credito).filter(pagada='0').order_by('numero_cuota')
        deuda=0
        capital=0
        sw = True
        for det in detalle:
            if sw:
                capital=det.capital
                sw = False
            deuda = deuda + det.monto_cuota - det.abono_a_cuota
            # aqui debo ver de donde saco el monto que se debe a capita, creo que seria el monto menos lo amortizado
            # o la columna capital, ya lo veo   28/09/2021
            #capital = capital + det.capital
        cred = creditos.objects.get(cod_credito=v_cod_credito)
        cred.saldo_credito = deuda
        cred.capital = capital
        if deuda==0:
            cred.pagada='1'
        cred.save()

        return super().form_valid(form)




    def get_context_data(self, **kwargs):
        # en esta variabla context_data coloco el contecto de la clase

        context_data = super(CreditosPagoCreateView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario


        #En nrotc extaigo de los parametros el valor de nrotc, este lo asigno en urls
        v_cod_credito = self.kwargs['codigo']
        m_credito=creditos.objects.get(cod_credito=v_cod_credito)
        v_articulo=m_credito.articulo
        context_data['Articulo']=v_articulo
        #en context_data creo una entrada llamanda Tarjeta y le asigno el parametro con que se llamo la vista
        detalle = detalle_creditos.objects.filter(cod_credito=v_cod_credito).filter(pagada='0').order_by('numero_cuota')
        a_pagar=0
        hoy=date.today()
        mes_hoy=hoy.month
        ano_hoy=hoy.year
        ano_mes_hoy=ano_hoy*100+mes_hoy
        for det in detalle:
            ano_mes_cuota=det.ano*100+det.mes
            if ano_mes_cuota <= ano_mes_hoy:
                a_pagar=a_pagar+det.monto_cuota - det.abono_a_cuota
        if a_pagar == 0:
            mes_hoy=mes_hoy+1
            if mes_hoy==13:
                ano_hoy=ano_hoy+1
            ano_mes_hoy=ano_hoy*100+mes_hoy
            for det in detalle:
                ano_mes_cuota=det.ano*100+det.mes
                if ano_mes_cuota <= ano_mes_hoy:
                    a_pagar=a_pagar+det.monto_cuota - det.abono_a_cuota
        context_data['aPagar']=a_pagar
        #retorno el contexto modificado
        return context_data


class CreditosUpdateView(UpdateView):
    fields = ['cod_entidad','cod_credito','articulo','quincena','image']
    template_name= 'creditos/creditos_form.html'
    #template_name= 'gastos/gastos_update.html'
    model = creditos
    context_object_name='creditos'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super(CreditosUpdateView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data


class CreditosCreateView(CreateView):
    fields = ['cod_entidad','cod_credito','articulo','fecha_compra','costo_original','tasa_interes','plazo_meses','quincena','image']
    template_name= 'creditos/creditos_form.html'
    #template_name= 'gastos/gastos_update.html'
    model = creditos
    context_object_name='creditos'

    def form_valid(self, form):
        #Aqui se procesa luego que la forma es validada
        v_costo_original=form.instance.costo_original
        v_costo=form.instance.costo_original
        v_plazo=form.instance.plazo_meses
        v_tasa=form.instance.tasa_interes
        v_cod_credito=form.instance.cod_credito
        v_fecha=form.instance.fecha_compra
        iva=float(1.16)
        v_tasa=float(v_tasa)
        v_tem1=v_tasa/100.00
        v_tem=v_tem1/12.00
        v_tasa_calculo=v_tem/iva
        v_tasa_calculo=round(Decimal(v_tasa_calculo),6)
        v_tem=round(Decimal(v_tem),6)
        # uso la tasa SIN IVA, estamos asumientdo que la tasa_interes ya tiene IVA
        if v_tasa==0:
            v_cuota=v_costo_original/v_plazo
        else:
            v_cuota=(v_costo*(v_tem*(1+v_tem)**v_plazo))/(((1+v_tem)**v_plazo)-1)

        form.instance.usuario = self.request.user

        v_mes=v_fecha.month+1
        v_ano=v_fecha.year
        v_deuda_total=0
        i=1
        while i <=v_plazo:
            if v_mes==13:
                v_mes=1
                v_ano=v_ano+1
            v_intereses=v_costo*v_tasa_calculo
            v_iva=v_intereses*16/100  #IVA fijo en 16, se puede parametrizar
            v_amortiza=v_cuota-v_intereses-v_iva
            v_saldo=v_costo-v_amortiza

            #aqui insertas
            dc=detalle_creditos(cod_credito=v_cod_credito,
                                 numero_cuota=i,
                                 mes=v_mes,
                                 ano=v_ano,
                                 pagada=0,
                                 monto_cuota=v_cuota,
                                 intereses=v_intereses,
                                 iva_intereses=v_iva,
                                 amortiza=v_amortiza,
                                 capital=v_saldo,
                                 usuario = self.request.user

                                 )
            v_deuda_total=v_deuda_total+v_cuota
            dc.save()
            v_mes=v_mes+1

            #-----
            v_costo=v_saldo
            i=i+1


        form.instance.saldo_credito=v_deuda_total
        form.instance.capital=v_costo_original
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super(CreditosCreateView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data


#
#  con este tipo de vista puedo enviar 2 o mas modelos al template
#defino dos objetos con los modelos filtrados de acuerdo a los parametros (codigo)
# y los uno en una variable de contexto para enviarlo al render
# en el template los uso utilizando los nombres de los objetos filtrados (creditoDisplay
# solo trae un registro y detalleDisplay varios)
def CreditoDetalle(request, codigo):
    # con get solo me traigo un registro, solo debe cumplirse la condicion para un registro
    creditoDisplay = creditos.objects.get(cod_credito=codigo)
    # con filter me traigo un QuerySet iterable en el template
    detalleDisplay = detalle_creditos.objects.filter(cod_credito=codigo).order_by('numero_cuota')
    _userid = request.user.id
    id_usuario = User.objects.get(id=_userid)
    usuario = {'nombre_usuario' : id_usuario.username,
               'user_imagen' : id_usuario.profile.image
    }

    context ={'creditoDisplay':creditoDisplay,'detalleDisplay':detalleDisplay,'Usuario':usuario}
    return render(request, 'creditos\creditos_detail.html',context)






class CreditosDeleteView(DeleteView):
    model = creditos
    success_url = '/creditos/creditos/'  # luego de borrar va a home
    template_name ='creditos/creditos_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        obj = super(CreditosDeleteView, self).get_object()

        cod_cred=obj.cod_credito
        # falta modificar los montos y borrar la imagen

        movim=detalle_creditos.objects.filter(cod_credito=cod_cred)


        movim.delete()

        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


    def get_context_data(self, **kwargs):
        context_data = super(CreditosDeleteView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data
