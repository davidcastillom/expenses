from django.views.generic import ListView, UpdateView,DetailView, CreateView,DeleteView
from registro.models import tipos
from django.contrib.auth.models import User

# Create your views here.

class TiposListView(ListView):
    model = tipos
    template_name= 'tipos/tipos_list.html'
    context_object_name='tipos'

    def get_context_data(self, **kwargs):
        context_data = super(TiposListView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data

class TiposUpdateView(UpdateView):
    model = tipos
    fields = ['tipo','descripcion','busqueda']
    template_name= 'tipos/tipos_form.html'
    #template_name= 'tipos/tipos_update.html'
    #context_object_name='tipos'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super(TiposUpdateView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data

class TiposCreateView(CreateView):
    model = tipos
    fields = ['tipo','descripcion','busqueda']
    template_name= 'tipos/tipos_form.html'
    #template_name= 'tipos/tipos_update.html'
    #context_object_name='tipos'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super(TiposCreateView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data

class tiposDetalle(DetailView):
    model = tipos     # aqui si vamos a usar el por defecto <app>/<model>_<iwtype>.html
    fields = ['tipo','descripcion','busqueda']
    template_name= 'tipos/tipo_detail.html'
    context_object_name='tipos'


    def get_context_data(self, **kwargs):
        context_data = super(tiposDetalle, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data

class TiposDetailView(DetailView):
    model = tipos     # aqui si vamos a usar el por defecto <app>/<model>_<iwtype>.html
    #fields = ['id','tipo','descripcion']
    fields = ['tipo','descripcion','busqueda']
    template_name= 'tipos/tipo_detail.html'
    context_object_name='tipos'


    def get_context_data(self, **kwargs):
        context_data = super(TiposDetailView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data

class TiposDeleteView(DeleteView):
    model = tipos     # aqui si vamos a usar el por defecto <app>/<model>_<iwtype>.html
    success_url = '/tipos/tipodeuda/'  # luego de borrar va a home
    template_name ='tipos/tipos_confirm_delete.html'


    def get_context_data(self, **kwargs):
        context_data = super(TiposDeleteView, self).get_context_data(**kwargs)
        _userid = self.request.user.id
        id_usuario = User.objects.get(id=_userid)
        usuario = {'nombre_usuario' : id_usuario.username,
                   'user_imagen' : id_usuario.profile.image
        }
        context_data['Usuario']=usuario
        return context_data
