from django.shortcuts import render
from django.http import HttpResponse
from .models import (maestro,
                     tipos,
                     gastos,
                     factura_gastos,
                     tarjetas_credito,
                     entidad,
                     creditos,
                     detalle_creditos,
                     pagos, Profile
)
from django.contrib.auth.models import User
from datetime import date, time, datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.auth.decorators import login_required


v_gasto=gastos.objects.all().order_by('tipo','descripcion', 'quincena')


def principal(request):


    # -------------------------------------------
    #   Titulos
    meses = [{1,"enero"},
             {2,"febrero"},
             {3,"marzo"},
             {4,"abril"},
             {5,"mayo"},
             {6,"junio"},
             {7,"julio"},
             {8,"agosto"},
             {9,"septiembre"},
             {10,"octubre"},
             {11,"noviembre"},
             {12,"diciembre"}]
    meses = ["enero","febrero",
             "marzo","abril",
             "mayo","junio",
             "julio","agosto",
             "septiembre","octubre",
             "noviembre","diciembre"]
    ult_dia = [31,28,31,30,31,30,31,31,30,31,30,31]
    hoy=date.today()
    if hoy.day>15:
        # veo la segunda quincena del mes y la primera quincena del mes que viene
        fecha_ini_1q = date(hoy.year, hoy.month, 16)
        dia=ult_dia[hoy.month-1]
        fecha_fin_1q = date(hoy.year, hoy.month, dia)


        mes=meses[hoy.month-1]

        if hoy.month==12:
            mes2q=1
            mes2="enero"
            ano2=hoy.year+1
        else:
            mes2q=hoy.month+1
            mes=meses[hoy.month]
            ano2=hoy.year
        fecha_ini_2q = date(ano2, mes2q, 1)
        fecha_fin_2q = date(ano2, mes2q, 15)

        Titulo1="30"+" "+mes
        Titulo2="15"+" "+mes
    else:
        # veo la primera y segunda quincena del mes en curso
        mes=meses[hoy.month-1]
        Titulo1="15"+" "+mes
        Titulo2="30"+" "+mes
        fecha_ini_1q = date(hoy.year, hoy.month, 1)
        fecha_fin_1q = date(hoy.year, hoy.month, 15)
        fecha_ini_2q = date(hoy.year, hoy.month, 16)
        dia=ult_dia[hoy.month-1]
        fecha_fin_2q = date(hoy.year, hoy.month, dia)

    titulos={"t1": Titulo1,
             "t2": Titulo2}
    #------------------------------------

    # Salida del principal se puede mejorar
    items=[]
    antDesc = "Primera"

    sw=0
    Total_aPrimQuinc=float(0.00)
    Total_aSeguQuinc=0.00
    Total_pPrimQuinc=0.00
    Total_pSeguQuinc=0.00

    for gasto in v_gasto:
        aPrimQuinc=0.00
        aSeguQuinc=0.00
        pPrimQuinc=0.00
        pSeguQuinc=0.00
        aDesc=gasto.descripcion
        if gasto.tipo.busqueda=='Fijo':
            if gasto.quincena==1:
                aPrimQuinc=gasto.monto
            elif gasto.quincena==2:
                aSeguQuinc=gasto.monto
            else:
                aPrimQuinc=gasto.monto
                aSeguQuinc=gasto.monto2
        elif gasto.tipo.busqueda=='Factura':
            v_factura=factura_gastos.objects.all().filter(clave=gasto.clave).filter(pagada=0)
            for v_fact in v_factura:
                if v_fact.quincena==1:
                    aPrimQuinc=aPrimQuinc+float(v_fact.monto)
                else:
                    aSeguQuinc=aSeguQuinc+float(v_fact.monto)

            # vamos  a ver si sirve
            v_factura=factura_gastos.objects.all().filter(clave=gasto.clave).filter(pagada=1).filter(fecha_pago__range=(fecha_ini_1q,fecha_fin_2q))
            for v_fact in v_factura:
                if v_fact.quincena==1:
                    aPrimQuinc=aPrimQuinc+float(v_fact.monto)
                else:
                    aSeguQuinc=aSeguQuinc+float(v_fact.monto)


        elif gasto.tipo.busqueda=='Tarjeta de Credito':
            try:
                v_tcs=tarjetas_credito.objects.get(clave=gasto.clave)
                p1=v_tcs.pago_proyectado
                p2=v_tcs.pago_proyectado2
            except ObjectDoesNotExist:
                p1 = 0.00
                p2 = 0.00
                pass
            if gasto.quincena==1:
                aPrimQuinc=p1
                aSeguQuinc=p2
            else:
                aPrimQuinc=p2
                aSeguQuinc=p1



        elif gasto.tipo.busqueda=='Credito':
            try:
                v_entidad=entidad.objects.get(clave=gasto.clave)
                v_creditos=creditos.objects.filter(cod_entidad=v_entidad.cod_entidad)

                aPrimQuinc=0.00
                aSeguQuinc=0.00

                for v_cred in v_creditos:
                    v_detalle_creditos =detalle_creditos.objects.filter(cod_credito=v_cred.cod_credito).filter(pagada='0').order_by('numero_cuota').first()
                    if v_cred.quincena==1:
                        aPrimQuinc=aPrimQuinc+float(v_detalle_creditos.monto_cuota)
                    else:
                        aSeguQuinc=aSeguQuinc+float(v_detalle_creditos.monto_cuota)
            except ObjectDoesNotExist:
                pPrinQuinc=0.00
                pSeguQuinc=0.00
                pass

                # ya tienes la quincena en creditos. usala para repartir ell gasto=
                        #PAGOS
        try:
            v_pago=pagos.objects.all().filter(clave=gasto.clave).filter(fecha_pago__range=(fecha_ini_1q,fecha_fin_2q))
            #v_pago=pagos.objects.filter(Q(clave=gasto.clave),Q(fecha_pago>=fecha_ini_1q),Q(fecha_pago<=fecha_fin_2q))
            for pag in v_pago:
                if(pag.fecha_pago>=fecha_ini_1q and pag.fecha_pago<=fecha_fin_1q):
                    pPrimQuinc=pPrimQuinc+float(pag.monto_pago)
                else:
                    pSeguQuinc=pSeguQuinc+float(pag.monto_pago)
        except ObjectDoesNotExist:
            pPrinQuinc=0.00
            pSeguQuinc=0.00
            pass
        Total_aPrimQuinc=float(Total_aPrimQuinc)+float(aPrimQuinc)
        Total_aSeguQuinc=float(Total_aSeguQuinc)+float(aSeguQuinc)
        Total_pPrimQuinc=Total_pPrimQuinc+pPrimQuinc
        Total_pSeguQuinc=Total_pSeguQuinc+pSeguQuinc
        items.append({
            'titulo' : aDesc,
            'Q1_prev' : aPrimQuinc,
            'Q1_pago' : pPrimQuinc,
            'Q2_prev' : aSeguQuinc,
            'Q2_pago' : pSeguQuinc})
    totales={"q1a": Total_aPrimQuinc,
             "q2a": Total_aSeguQuinc,
             "q1p": Total_pPrimQuinc,
             "q2p": Total_pSeguQuinc }
    v_Quincena1 =  11471.16
    v_Quincena2 = 14282.70
    sueldo={"sQuinc1":v_Quincena1,
            "sQuinc2":v_Quincena2}
    queda={"q1a" : v_Quincena1 - Total_aPrimQuinc,
           "q2a" : v_Quincena2 - Total_aSeguQuinc}

    _userid = request.user.id
    id_usuario = User.objects.get(id=_userid)
    usuario = {'nombre_usuario' : id_usuario.username,
               'user_imagen' : id_usuario.profile.image
    }

    context = {
        'items' : items,
        'Sueldo' : sueldo,
        'Titulos' : titulos,
        'Totales' : totales,
        'Queda' : queda,
        'Usuario' : usuario
    }
    return render(request, 'registro/principal.html', context)

def index(request):
    return HttpResponse("Hola es la pagina de Registro")



def gastos(request):
    return HttpResponse("Pagina para configurar y cargar Gastos")

def crear_gasto(request):
    return HttpResponse("pagina para crear un gasto nuevo")

def crear_gasto_variable(request, id_gasto):
    return HttpResponse("Crear gasto variable Nro: " % id_gasto)
# Create your views here.
