from django.urls import path
from . views import GastosListView, GastosCreateView, GastosUpdateView, GastosDetailView,GastosDeleteView,GastosPagoCreateView

from . import views

urlpatterns = [
    path('gastosfijos/', GastosListView.as_view(), name='gastos_fijos'),
    path('gastosfijos/<str:pk>', GastosDetailView.as_view(), name='gastos_detail'),
    path('gastosfijos/<str:pk>/update', GastosUpdateView.as_view(), name='gastos_update'),
    path('gastosfijos/new/', GastosCreateView.as_view(), name='gastos_crear'),
    path('gastosfijos/<str:pk>/delete/', GastosDeleteView.as_view(), name='gastos_delete'),
    path('gastosfijos/new/pagar', GastosPagoCreateView.as_view(), name='gastos_pagar'),
    # principal-home es un nombre que puede ser usado para referenciar esta url
]
