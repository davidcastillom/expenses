from django.urls import path
from . views import (FacturasListView,
                    FacturasCreateView,
                    FacturasUpdateView,
                    FacturasPagarView,
                    FacturasDetailView,
                    FacturasDeleteView
)

from . import views

urlpatterns = [
    path('carga_facturas/', FacturasListView.as_view(), name='carga_facturas'),
    path('carga_facturas/<str:pk>', FacturasDetailView.as_view(), name='carga_facturas_detail'),
    path('carga_facturas/<str:pk>/update', FacturasUpdateView.as_view(), name='carga_facturas_update'),
#    path('pagar_facturas/<str:pk>/update', views.pagar_factura2, name='carga_facturas_pagar'),
    path('pagar_facturas/<str:pk>/update', FacturasPagarView.as_view(), name='carga_facturas_pagar'),
#    path('carga_facturas/new/', FacturasCreateView.as_view(), name='carga_facturas_crear'),
    path('carga_facturas/new/', FacturasCreateView.as_view(), name='carga_facturas_crear'),
    path('carga_facturas/<str:pk>/delete/', FacturasDeleteView.as_view(), name='carga_facturas_delete'),
    # principal-home es un nombre que puede ser usado para referenciar esta url
]
