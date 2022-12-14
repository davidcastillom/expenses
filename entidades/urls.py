from django.urls import path
from . views import (EntidadesListView,
                     EntidadesDetailView,
                     EntidadesCreateView,
                     EntidadesUpdateView,
                     EntidadesDeleteView,
                     EntidadDetalle
)

from . import views

urlpatterns = [
    path('entidades/', EntidadesListView.as_view(), name='entidades'),
    path('entidades/new/', EntidadesCreateView.as_view(), name='entidades_crear'),
    path('entidades/<str:pk>/', EntidadDetalle, name='entidades_detail'),
    #path('entidades/<str:pk>', EntidadesDetailView.as_view(), name='entidades_detail'),
    path('entidades/<str:pk>/update', EntidadesUpdateView.as_view(), name='entidades_update'),
#    path('creditos/<str:pk>/update', FacturasPagarView.as_view(), name='creditos_pagar'),
    path('entidades/<str:pk>/delete/', EntidadesDeleteView.as_view(), name='entidades_delete'),

]
