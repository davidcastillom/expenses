from django.shortcuts import render
from django.views.generic import ListView, UpdateView,DetailView, CreateView,DeleteView
from registro.models import movimientos_tc,tarjetas_credito
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

class MovTCDetailView(UpdateView):
    model = movimientos_tc
    fields = ['numerotc','tipo_mov','fecha','descripcion','monto']
    template_name= 'movimientos_tc/movimientos_tc_detail.html'
    context_object_name='movtc'

class MovTCListFiltradaView(ListView):
    model = movimientos_tc
    template_name= 'movimientos_tc/movimientos_tc_list.html'
    context_object_name='movtc'
    fields = ['numerotc','tipo_mov','fecha','descripcion','monto']

    def get_queryset(self):
        return movimientos_tc.objects.filter(numerotc = self.kwargs['nrotc'])
# Filtrado por el parametro que se le pasa por la pagina que lo llama, ver en URLS la recepcion de la variable nrotc
    def get_context_data(self, **kwargs):
        context_data = super(MovTCListFiltradaView, self).get_context_data(**kwargs)
        nrotc = self.kwargs['nrotc']
        context_data['Tarjeta']=nrotc
        return context_data

class MovTCCreateView(CreateView):
    model = movimientos_tc
    template_name= 'movimientos_tc/movimientos_tc_form.html'
    fields = ['tipo_mov','fecha','descripcion','monto']
    context_object_name='movtc'



# aqui defino la ruta de retorno al crear el registro en ludar de ponerlo en el modelo
# lo hago aca ya que en el modelo no puedo pasarle el parametro ya que viene de otra
#operacion
    def get_success_url(self, **kwargs):
        context_data = super(MovTCCreateView, self).get_context_data(**kwargs)
        nrotc = self.kwargs['nrotc']
        return reverse('movimientostc_f', kwargs={'nrotc': nrotc})

    #Esto lo hago para poder mostrar en el tempate el numero de la tarjeta
    def get_context_data(self, **kwargs):
        # en esta variabla context_data coloco el contecto de la clase
        context_data = super(MovTCCreateView, self).get_context_data(**kwargs)
        #En nrotc extaigo de los parametros el valor de nrotc, este lo asigno en urls
        nrotc = self.kwargs['nrotc']
        #en context_data creo una entrada llamanda Tarjeta y le asigno el parametro con que se llamo la vista
        context_data['Tarjeta']=nrotc
        #retorno el contexto modificado
        return context_data

    def form_valid(self, form):
        #Aqui se procesa luego que la forma es validada
        nrotc = self.kwargs['nrotc']
        form.instance.numerotc = nrotc

        form.instance.usuario = self.request.user

        monto=form.instance.monto
        tc=tarjetas_credito.objects.get(numerotc=nrotc)
        deuda=tc.deuda_total
        deuda=monto+deuda
        tc.deuda_total=deuda
        tc.save()

        return super().form_valid(form)

class MovTCUpdateView(UpdateView):
    model = movimientos_tc
    fields = ['tipo_mov','fecha','descripcion','monto']
    template_name= 'movimientos_tc/movimientos_tc_form.html'
    context_object_name='movtc'

    def get_initial(self):
        initial = super(MovTCUpdateView, self).get_initial()
        return initial

    def form_valid(self, form):
        obj = super(MovTCUpdateView, self).get_object()
        monto_orig=obj.monto

        form.instance.usuario = self.request.user

        monto=form.instance.monto
        nrotc=form.instance.numerotc

        tc=tarjetas_credito.objects.get(numerotc=nrotc)
        deuda=tc.deuda_total
        deuda=monto-monto_orig+deuda
        tc.deuda_total=deuda
        tc.save()

        return super().form_valid(form)


class MovTCDeleteView(DeleteView):
    model = movimientos_tc     # aqui si vamos a usar el por defecto <app>/<model>_<iwtype>.html
    success_url = '/tarjeta_credito/tarjeta_credito/'  # luego de borrar va a home
    template_name ='tarjeta_credito/tarjeta_credito_confirm_delete.html'


    # aqui estoy sobre escribiendo el metodo delete() para poder manipular la data antes
    # de borrar. el primer bloque hago lo que necesito , luego ejecuto los comados de borrar
    def delete(self, request, *args, **kwargs):
        obj = super(MovTCDeleteView, self).get_object()

        nrotc=obj.numerotc
        monto=obj.monto

        tc=tarjetas_credito.objects.get(numerotc=nrotc)
        deuda=tc.deuda_total
        deuda=deuda-monto
        tc.deuda_total=deuda
        tc.save()

        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)
