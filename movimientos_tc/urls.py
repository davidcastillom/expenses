from django.urls import path
from . views import MovTCListFiltradaView, MovTCCreateView,MovTCUpdateView,MovTCDetailView,MovTCDeleteView
from . import views

urlpatterns = [
    path('movimientos_tc/<str:nrotc>/', MovTCListFiltradaView.as_view(), name='movimientostc_f'),
    path('movimientos_tc/<str:nrotc>/new/', MovTCCreateView.as_view(), name='movimientos_tc_crear'),
    path('movimientos_tc/detail/<int:pk>/', MovTCDetailView.as_view(), name='movimientos_tc_detail'),
    path('movimientos_tc/<int:pk>//update', MovTCUpdateView.as_view(), name='movimientos_tc_update'),
    path('movimientos_tc/<int:pk>/delete/', MovTCDeleteView.as_view(), name='movimientos_tc_delete'),
    # principal-home es un nombre que puede ser usado para referenciar esta url
]
