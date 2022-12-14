

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from django.db.models import Q


BRADESCARD='Bradescard'
BBVA='BBVA'
SANTANDER='Santander'
CITI='City Banamex'
AMEX='American Express'
bancos_busqueda=((BRADESCARD,'Bradescard'),
    (BBVA,'BBVA'),
    (SANTANDER,'Santander'),
    (CITI,'City Banamex'),
    (AMEX,'American Express'))

TRANSFERENCIA='Transferencia'
PAGO_EN_LINEA='Pago en Linea'
PAGO_EN_TIENDA='Pago en Tienda'
PAGO_EN_FARMACIA='Pago en Farmacia'

formas_pago=((TRANSFERENCIA,'Transferencia'),
    (PAGO_EN_LINEA,'Pago en Linea'),
    (PAGO_EN_TIENDA,'Pago en Tienda'),
    (PAGO_EN_FARMACIA,'Pago en Farmacia'))

class maestro(models.Model):
    clave = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=20)
    tipo = models.CharField(max_length=1)  #1=gastos , 2=creditos , 3 = tarjetas de credito
    quincena = models.CharField(max_length=1)
    mes = models.CharField(max_length=2)
    ano = models.IntegerField()
    monto_a_pagar = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    monto_pagado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion


class tipos(models.Model):
    FIJO='Fijo'
    FACTURA='Factura'
    TIENDA='Credito Tienda'
    TC='Tarjeta de Credito'
    BANCO='Banco'
    CREDITO='Credito'
    valores_busqueda=((FIJO,'Fijo'),
                      (FACTURA,'Factura'),
                      (TIENDA,'Credito Tienda'),
                      (TC,'Tarjeta de Credito'),
                      (BANCO,'Banco'),
                      (CREDITO,'Credito'))
    tipo = models.CharField(max_length=1,default=" ", primary_key=True)
    descripcion = models.CharField(max_length=20, default=" ")
    busqueda = models.CharField(max_length=20, default='Fijo', choices=valores_busqueda)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.busqueda

    def get_absolute_url(self):
        return reverse('tipos_deuda')

# Gastos son fijos en monto, no varian o casi no varian
class gastos(models.Model):
    PRIMERA=1
    SEGUNDA=2
    AMBAS=3
    quincenas=((PRIMERA,'Primera'),
                      (SEGUNDA,'Segunda'),
                      (AMBAS,'Ambas'))
    clave = models.AutoField(primary_key=True)
    #tipo = models.CharField(max_length=1,default=" ")
    tipo = models.ForeignKey(tipos, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=30, default=" ") # Mariann, TOtal play
    monto = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    dia_pagar = models.IntegerField(default=15) #dia del mes que se debe pagar
    quincena = models.IntegerField(default=1, choices=quincenas) #en cual quincena lo añado
    monto2 = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    dia_pagar2 = models.IntegerField(default=30) #, choices={('1',15),('2',16)}) #16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31}) #dia del mes que se debe pagar
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion

    def get_absolute_url(self):
        return reverse('gastos_fijos')


# Los gastos_factura son cosas como Luz, cable, etc que son fijos, pero no necesariamente el mimo monto
class factura_gastos(models.Model):

    clave = models.ForeignKey(gastos, on_delete=models.CASCADE, limit_choices_to={'tipo': 'B'} )
    # 08/09/2021 aqui resolvi que el filtro de la seleccion del tipo de gasto sea solo los que llevan factura
    #pero, deberia buscar que filtre los varios que pueden llever facturas. DCM
    factura = models.CharField(max_length=15,primary_key=True)
    fecha= models.DateField()
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    pagada = models.CharField(max_length=1, default=0)
    fecha_pago = models.DateField(default=date.today)
    image = models.ImageField(default='/facturas/default.jpg', upload_to='facturas')
    forma_de_pago=models.CharField(max_length=20, choices=formas_pago)
    folio=models.CharField(max_length=15)
    quincena = models.IntegerField(default=1)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

#    def save(self):    #puedes sobreescribir el metodo
#        super().save()

#        img= Image.open(self.image.path)

#        if img.height > 300 or img.width >300:
#            output_size = (300, 300)
#            img.thumbnail(output_size)
#            img.save(self.image.path)

    def __str__(self):
        return self.factura

    def get_absolute_url(self):
        return reverse('carga_facturas')

class tarjetas_credito(models.Model):
    numerotc = models.CharField(max_length=20, default=' ', primary_key=True)
    clave = models.ForeignKey(gastos, on_delete=models.CASCADE, limit_choices_to={'tipo': 'C'} )
    nombretc = models.CharField(max_length=30, default=' ')
    banco = models.CharField(max_length=30, default=' ', choices=bancos_busqueda)
    limite = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha_vencimiento = models.DateField()
    dia_corte = models.IntegerField(default=1)
    dia_pagar_antes = models.IntegerField(default=1)
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    image = models.ImageField(default='/tarjetas/default.jpg', upload_to='tarjetas')
    pago_proyectado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pago_proyectado2 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pago_minimo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deuda_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # el pago minimo debemos hacerlo calculado y por defecto lo ponemos en pago proyectado
    # si vas a diferir el pago en dos quincenas, lo que colques en pago_proyectado sera
    #lo que se pague en la quincena que dice el gasto y lo otro en la otra quincena.
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.numerotc

    def get_absolute_url(self):
        return reverse('tarjeta_credito')

class movimientos_tc(models.Model):
    PAGO='Pago'
    COMPRA ='Compra'
    INTERESES ='Intereses'
    IVA ='IVA'
    ANUALIDAD ='Anualidad'
    valores_busqueda=((PAGO,'Pago'),
        (COMPRA,'Compra'),
        (INTERESES ,'Intereses'),
        (IVA ,'IVA'),
        (ANUALIDAD ,'Anualidad'))
    auto_increment_id=models.AutoField(primary_key=True)
    numerotc = models.CharField(max_length=20, default=' ')
    tipo_mov = models.CharField(max_length=30, default='Compra', choices=valores_busqueda)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=30, default='compra')
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('tarjeta_credito')
 #Q objects       Q('D' | 'E')
# tipos.objects.filter(Q(busqueda='Credito'))
class entidad(models.Model):
    clave = models.ForeignKey(gastos, on_delete=models.CASCADE, limit_choices_to={'tipo': 'E','tipo': 'D'})
    cod_entidad= models.AutoField(primary_key=True)
    entidad = models.CharField(max_length=30)      #aqui seria Coppel, Liverpool, prestamo personal lo que sea a cuotas fijas
    image = models.ImageField(default='/entidad/default.jpg', upload_to='entidad')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.entidad

    def get_absolute_url(self):
        return reverse('entidades')

class creditos(models.Model):
    cod_entidad = models.ForeignKey(entidad, on_delete=models.CASCADE)
    cod_credito =  models.IntegerField(primary_key=True)
    articulo = models.CharField(max_length=30)     # que si una sierra, o prestamo personal, o pasajes
    costo_original = models.DecimalField(max_digits=12, decimal_places=2)
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2)
    plazo_meses = models.IntegerField(default=12)
    costo_credito  = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    image = models.ImageField(default='/creditos/default.jpg', upload_to='creditos')
    pagada = models.CharField(max_length=1,default=0)
    saldo_credito = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    capital = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha_compra = models.DateField(default=date.today)
    quincena = models.IntegerField(default=1)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('creditos')

class detalle_creditos(models.Model):
    id_credito = models.AutoField(primary_key=True)
    #cod_credito = models.ForeignKey(creditos, on_delete=models.CASCADE)
    cod_credito = models.IntegerField()
    numero_cuota = models.IntegerField()
    mes = models.IntegerField(default=1)
    ano = models.IntegerField(default=2021)
    pagada = models.CharField(max_length=1,default=0)
    fecha_pago = models.DateField(verbose_name="Fecha de Pago", null=True)
    folio=models.CharField(max_length=15,default=" ")
    forma_de_pago=models.CharField(max_length=20, choices=formas_pago, default='Pago en Linea')
    monto_cuota = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    abono_a_cuota = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    intereses = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    iva_intereses = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amortiza = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    capital = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class pagos(models.Model):
    id_pago = models.AutoField(primary_key=True)
    fecha_pago = models.DateField()
    cod_credito = models.IntegerField(default=0)
    factura = models.CharField(max_length=15,default=" ")
    numerotc = models.CharField(max_length=20, default=' ')
    clave = models.ForeignKey(gastos, on_delete=models.CASCADE)   # solo para pago de gastos fijos
    forma_de_pago=models.CharField(max_length=20, choices=formas_pago, default='Pago en Linea')
    monto_pago = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    folio=models.CharField(max_length=15,default=" ")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'(self.user.username) Profile'
