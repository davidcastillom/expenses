from django.urls import path
from . views import (TarjetasCreditoListView,
                    TarjetasCreditoCreateView,
                    TarjetasCreditoUpdateView,
                    TarjetasCreditoDetailView,
                    TarjetasCreditoDeleteView,
                    TarjetasCreditosPagoCreateView
)
from . import views

urlpatterns = [
    path('tarjeta_credito/', TarjetasCreditoListView.as_view(), name='tarjeta_credito'),
    path('tarjeta_credito/<str:pk>', TarjetasCreditoDetailView.as_view(), name='tarjeta_credito_detail'),
    path('tarjeta_credito/<str:pk>/update', TarjetasCreditoUpdateView.as_view(), name='tarjeta_credito_update'),
    path('tarjeta_credito/new/', TarjetasCreditoCreateView.as_view(), name='tarjeta_credito_crear'),
    path('tarjeta_credito/<str:pk>/delete/', TarjetasCreditoDeleteView.as_view(), name='tarjeta_credito_delete'),
    path('tarjeta_credito/new/<str:nrotc>/', TarjetasCreditosPagoCreateView.as_view(), name='tarjeta_credito_pagar'),
]
