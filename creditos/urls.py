from django.urls import path
from . views import (CreditosListView,
                    CreditosCreateView,
                    CreditosUpdateView,
                    CreditosDeleteView,
                    CreditoDetalle,
                    CreditosPagoCreateView
)

from . import views

urlpatterns = [
    path('creditos/', CreditosListView.as_view(), name='creditos'),
    #path('creditos/<str:pk>', CreditosUnionDetailView.as_view(), name='creditos_detail'),
    path('creditos/<int:codigo>/', CreditoDetalle, name='creditos_detail'),
    path('creditos/new/<int:codigo>/', CreditosPagoCreateView.as_view(), name='creditos_pagar'),
    #path('creditos/<str:pk>',CreditoDetalle, name='creditos_detail')
    #path('creditos/<str:pk>', CreditosDetailView.as_view(), name='creditos_detail'),
    path('creditos/<int:pk>/update', CreditosUpdateView.as_view(), name='creditos_update'),
#    path('creditos/<str:pk>/update', FacturasPagarView.as_view(), name='creditos_pagar'),
    path('creditos/new/', CreditosCreateView.as_view(), name='creditos_crear'),
    path('creditos/<int:pk>/delete/', CreditosDeleteView.as_view(), name='creditos_delete'),

]
