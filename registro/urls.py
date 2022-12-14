from django.urls import path

from . import views

urlpatterns = [
    path('', views.principal, name='principal-home'),
#    # principal-home es un nombre que puede ser usado para referenciar esta url
#    path('', views.index, name='index'),
#    path('', views.gastos, name='gastos'),
#    path('', views.crear_gasto, name='crear_gasto'),
#    path('<int:id_gasto>/crear_gasto_variable/', views.crear_gasto_variable, name='crear_gasto_variable'),
]
