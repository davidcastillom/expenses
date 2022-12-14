from django.urls import path
from . views import TiposListView, TiposCreateView, TiposUpdateView, TiposDetailView,TiposDeleteView

from . import views

urlpatterns = [
    path('tipodeuda/', TiposListView.as_view(), name='tipos_deuda'),
    path('tipos/<str:pk>', TiposDetailView.as_view(), name='tipo_detail'),
    path('tipos/<str:pk>/update', TiposUpdateView.as_view(), name='tipo_update'),
    path('tipos/new/', TiposCreateView.as_view(), name='tipo_crear'),
    path('tipos/<str:pk>/delete/', TiposDeleteView.as_view(), name='tipo_delete'),
    # principal-home es un nombre que puede ser usado para referenciar esta url

]
