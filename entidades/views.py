from django.views.generic import ListView, UpdateView,DetailView, CreateView,DeleteView
from registro.models import entidad, creditos
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User

# Create your views here.
# [clave,numerotc, nombretc, limite, fecha_vencimiento, dia_corte, dia_pagar_antes, tasa_interes, image, pago_proyectado, pago_minimo, deuda_total ]





class EntidadesListView(ListView):
    template_name= 'entidades/entidades_list.html'
    model = entidad
    context_object_name='entidades'

    def get_queryset(self):  #aqui vamos a filtrar por Usuario
         #obtengo el usuario logueado con self.request.user
         return entidad.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context_data = super(EntidadesListView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data


class EntidadesUpdateView(UpdateView):
    fields = ['clave',  'entidad', 'image']
    template_name= 'entidades/entidades_form.html'
    #template_name= 'gastos/gastos_update.html'
    model = entidad
    context_object_name='entidades'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super(EntidadesUpdateView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data


class EntidadesCreateView(CreateView):
    fields = ['clave',  'entidad', 'image']
    template_name= 'entidades/entidades_form.html'
    #template_name= 'gastos/gastos_update.html'
    model = entidad
    context_object_name='entidades'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super(EntidadesCreateView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data


class EntidadesDetailView(DetailView):
        # aqui si vamos a usar el por defecto <app>/<model>_<iwtype>.html
    fields = ['clave', 'entidad', 'image']
    template_name= 'entidades/entidades_detail.html'
    model = entidad
    context_object_name='entidades'

    def get_context_data(self, **kwargs):
        context_data = super(EntidadesDetailView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data


def EntidadDetalle(request, pk):
    # con get solo me traigo un registro, solo debe cumplirse la condicion para un registro
    entidadDisplay = entidad.objects.get(cod_entidad=pk)
    # con filter me traigo un QuerySet iterable en el template
    creditoDisplay = creditos.objects.filter(cod_entidad=pk)  #.order_by('numero_cuota')
    _userid = request.user.id
    id_usuario = User.objects.get(id=_userid)
    usuario = {'nombre_usuario' : id_usuario.username,
               'user_imagen' : id_usuario.profile.image
    }
    context ={'creditoDisplay':creditoDisplay,'entidadDisplay':entidadDisplay, 'Usuario':usuario}
    return render(request, 'entidades\entidades_detail.html',context)




class EntidadesDeleteView(DeleteView):
    model = entidad
    success_url = '/entidades/entidades/'  # luego de borrar va a home
    template_name ='entidades/entidades_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context_data = super(EntidadesDeleteView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data
