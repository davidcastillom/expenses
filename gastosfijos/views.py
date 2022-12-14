from django.views.generic import ListView, UpdateView,DetailView, CreateView,DeleteView
from registro.models import gastos, pagos, gastos
from django.urls import reverse
from django.contrib.auth.models import User

# Create your views here.

class GastosListView(ListView):
    model = gastos
    template_name= 'gastosfijos/gastosfijos_list.html'
    queryset = gastos.objects.order_by('tipo','clave')
    context_object_name='gastos'

    def get_context_data(self, **kwargs):
        context_data = super(GastosListView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data

class GastosUpdateView(UpdateView):
    model = gastos
    fields = ['clave', 'tipo','descripcion','quincena','monto','dia_pagar','monto2','dia_pagar2']
    template_name= 'gastosfijos/gastosfijos_form.html'
    #template_name= 'gastos/gastos_update.html'
    context_object_name='gastos'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super(GastosUpdateView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data

class GastosCreateView(CreateView):
    model = gastos
    fields =  ['clave', 'tipo','descripcion','quincena','monto','dia_pagar','monto2','dia_pagar2']
    template_name= 'gastosfijos/gastosfijos_form.html'
    #template_name= 'gastos/gastos_update.html'
    context_object_name='gastos'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super(GastosCreateView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data


class GastosDetailView(DetailView):
    model = gastos     # aqui si vamos a usar el por defecto <app>/<model>_<iwtype>.html
    fields =  ['clave', 'tipo','descripcion','quincena','monto','dia_pagar','monto2','dia_pagar2']
    template_name= 'gastosfijos/gastosfijos_detail.html'
    context_object_name='gastos'

    def get_context_data(self, **kwargs):
        context_data = super(GastosDetailView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data


class GastosDeleteView(DeleteView):
    model = gastos     # aqui si vamos a usar el por defecto <app>/<model>_<iwtype>.html
    success_url = '/gastosfijos/gastosfijos/'  # luego de borrar va a home
    template_name ='gastosfijos/gastosfijos_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context_data = super(GastosDeleteView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data


class GastosPagoCreateView(CreateView):
    fields = ['clave','forma_de_pago','fecha_pago','monto_pago','folio']
    template_name= 'gastosfijos/gastosfijos_pagar.html'
    #template_name= 'gastos/gastos_update.html'
    model = pagos
    context_object_name='pagos'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super(GastosPagoCreateView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data

# aqui defino la ruta de retorno al crear el registro en ludar de ponerlo en el modelo
# lo hago aca ya que en el modelo no puedo pasarle el parametro ya que viene de otra
#operacion
    def get_success_url(self):

        return reverse('principal-home')


# Create your views here.
