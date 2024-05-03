from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils import timezone
from django.conf import settings
from io import BytesIO
import qrcode
from django.core.files import File

# MODELOS

#--------------------------------USUARIO------------------------------------------------
class Usuario(AbstractUser):
    #id
    username = models.CharField(max_length=80, unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=60)
    nivel = models.IntegerField(null=True) 

    @classmethod
    def numeroRegistrados(self):
        return int(self.objects.all().count() )   

    @classmethod
    def numeroUsuarios(self,tipo):
        if tipo == 'administrador':
            return int(self.objects.filter(is_superuser = True).count() )
        elif tipo == 'usuario':
            return int(self.objects.filter(is_superuser = False).count() )


#-------------------------------- O P C I O N E S ------------------------------------------------

class Opciones(models.Model):
    #id
    moneda = models.CharField(max_length=20, null=True)
    valor_iva = models.IntegerField(unique=True)   
    nombre_negocio = models.CharField(max_length=25,null=True)
    mensaje_factura = models.TextField(null=True)

class Impuesto(models.Model):
    nombre = models.CharField(max_length=100)
    tasa = models.DecimalField(max_digits=5, decimal_places=2)  # Porcentaje del impuesto

    def __str__(self):
        return f"{self.nombre} ({self.tasa}%)"



#---------------------------------------------------------------------------------------

#-----------------------------------CATEGORIA-------------------------------------------
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre
#---------------------------------------------------------------------------------------

#------------------------------------------ T I P O --------------------------------------

class TipoProducto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'inventario_tipo'  # Especifica el nombre de la tabla existente

    def __str__(self):
        return self.nombre

#------------------------------------------------------------------------------------------

#-------------------------------PRODUCTO------------------------------------------------

class Producto(models.Model):
        #id
        decisiones =  [('1','Unidad'),('2','Kilo'),('3','Litro'),('4','Otros')]
        descripcion = models.CharField(max_length=40)
        precio = models.DecimalField(max_digits=9, decimal_places=2,null=True, blank=True)
        disponible = models.IntegerField(null=True)
        tipo = models.ForeignKey(TipoProducto, on_delete=models.SET_NULL, null=True, blank=True)
        codigo_barra = models.CharField(max_length=100, null=True, blank=True)  # Nuevo campo
        fecha_introduccion = models.DateField(default=timezone.now)
        fecha_vencimiento = models.DateField(default=timezone.now)
        categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=1)
        precio_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
        precio_maximo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
        codigo_barra = models.CharField(max_length=100, null=True, blank=True, unique=True)
        imagen_codigo_qr = models.ImageField(upload_to='codigos_qr/', null=True, blank=True)
        imagen_producto = models.ImageField(upload_to='imagenes_productos/', null=True, blank=True)
        ultima_actualizacion = models.DateTimeField(auto_now=True)


        def save(self, *args, **kwargs):
            qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
            qr.add_data(self.codigo_barra)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer)
            filename = f'qr_{self.codigo_barra}.png'
            filebuffer = File(buffer, name=filename)
            self.imagen_codigo_qr.save(filename, filebuffer, save=False)
            super().save(*args, **kwargs)

        

        @classmethod
        def numeroRegistrados(self):
            return int(self.objects.all().count() )
    

        @classmethod
        def productosRegistrados(self):
            objetos = self.objects.all().order_by('descripcion')
            return objetos


        @classmethod
        def preciosProductos(self):
            objetos = self.objects.all().order_by('id')
            arreglo = []
            etiqueta = True
            extra = 1

            for indice,objeto in enumerate(objetos):
                arreglo.append([])
                if etiqueta:
                    arreglo[indice].append(0)
                    arreglo[indice].append("------")
                    etiqueta = False
                    arreglo.append([])

                arreglo[indice + extra].append(objeto.id)
                precio_producto = objeto.precio
                if isinstance(precio_producto, str):
                    arreglo[indice + extra].append(precio_producto)
                else:
                    arreglo[indice + extra].append("%d" % precio_producto)  

            return arreglo 

        @classmethod
        def productosDisponibles(self):
            objetos = self.objects.all().order_by('id')
            arreglo = []
            etiqueta = True
            extra = 1

            for indice,objeto in enumerate(objetos):
                arreglo.append([])
                if etiqueta:
                    arreglo[indice].append(0)
                    arreglo[indice].append("------")
                    etiqueta = False
                    arreglo.append([])

                arreglo[indice + extra].append(objeto.id)
                productos_disponibles = objeto.disponible
                arreglo[indice + extra].append("%d" % (productos_disponibles) )  

            return arreglo 
#---------------------------------------------------------------------------------------





#------------------------------------------PRECIOS--------------------------------------
class PrecioScraping(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='precios_scraping')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fuente = models.CharField(max_length=100)
    fecha_obtencion = models.DateTimeField(auto_now_add=True)
    tienda_logo = models.URLField(max_length=255, null=True, blank=True)


    def __str__(self):
        return f"{self.producto} - {self.precio} ({self.fuente})"
    
#---------------------------------------------------------------------------------------

#------------------------------------------CLIENTE--------------------------------------
class Cliente(models.Model):
    #id
    cedula = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    direccion = models.CharField(max_length=200)
    nacimiento = models.DateField()
    telefono = models.CharField(max_length=20)
    telefono2 = models.CharField(max_length=20,null=True)
    correo = models.CharField(max_length=100)
    correo2 = models.CharField(max_length=100,null=True)

    @classmethod
    def numeroRegistrados(self):
        return int(self.objects.all().count() )

    @classmethod
    def cedulasRegistradas(self):
        objetos = self.objects.all().order_by('nombre')
        arreglo = []
        for indice,objeto in enumerate(objetos):
            arreglo.append([])
            arreglo[indice].append(objeto.cedula)
            nombre_cliente = objeto.nombre + " " + objeto.apellido
            arreglo[indice].append("%s. C.I: %s" % (nombre_cliente,self.formatearCedula(objeto.cedula)) )
 
        return arreglo   


    @staticmethod
    def formatearCedula(cedula):
        return format(int(cedula), ',d')        
#-----------------------------------------------------------------------------------------        



#-------------------------------------FACTURA---------------------------------------------
class Factura(models.Model):
    #id
    cliente = models.ForeignKey(Cliente,to_field='cedula', on_delete=models.CASCADE)
    fecha = models.DateField()
    sub_monto = models.DecimalField(max_digits=20,decimal_places=2)
    monto_general = models.DecimalField(max_digits=20,decimal_places=2)
    iva = models.ForeignKey(Opciones,to_field='valor_iva', on_delete=models.CASCADE)

    @classmethod
    def numeroRegistrados(self):
        return int(self.objects.all().count() )

    @classmethod
    def ingresoTotal(self):
        facturas = self.objects.all()
        total = 0

        for factura in facturas:
            total += factura.monto_general

        return total
#-----------------------------------------------------------------------------------------


#-------------------------------------DETALLES DE FACTURA---------------------------------
class DetalleFactura(models.Model):
    #id
    id_factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    sub_total = models.DecimalField(max_digits=20,decimal_places=2)
    total = models.DecimalField(max_digits=20,decimal_places=2)

    @classmethod
    def productosVendidos(self):
        vendidos = self.objects.all()
        totalVendidos = 0
        for producto in vendidos:
            totalVendidos += producto.cantidad

        return totalVendidos  

    @classmethod
    def ultimasVentas(self):
        objetos = self.objects.all().order_by('-id')[:10]

        return objetos
#---------------------------------------------------------------------------------------


#------------------------------------------PROVEEDOR-----------------------------------
class Proveedor(models.Model):
    #id
    cedula = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    direccion = models.CharField(max_length=200)
    nacimiento = models.DateField()
    telefono = models.CharField(max_length=20)
    telefono2 = models.CharField(max_length=20,null=True)
    correo = models.CharField(max_length=100)
    correo2 = models.CharField(max_length=100,null=True)

    @classmethod
    def cedulasRegistradas(self):
        objetos = self.objects.all().order_by('nombre')
        arreglo = []
        for indice,objeto in enumerate(objetos):
            arreglo.append([])
            arreglo[indice].append(objeto.cedula)
            nombre_cliente = objeto.nombre + " " + objeto.apellido
            arreglo[indice].append("%s. C.I: %s" % (nombre_cliente,self.formatearCedula(objeto.cedula)) )
 
        return arreglo 

    @staticmethod
    def formatearCedula(cedula):
        return format(int(cedula), ',d')  
#---------------------------------------------------------------------------------------    


#----------------------------------------PEDIDO-----------------------------------------
class Pedido(models.Model):
    #id
    proveedor = models.ForeignKey(Proveedor,to_field='cedula', on_delete=models.CASCADE)    
    fecha = models.DateField()
    sub_monto = models.DecimalField(max_digits=20,decimal_places=2)
    monto_general = models.DecimalField(max_digits=20,decimal_places=2)
    iva = models.ForeignKey(Opciones,to_field='valor_iva', on_delete=models.CASCADE)
    presente = models.BooleanField(null=True)

    @classmethod
    def recibido(self,pedido):
        return self.objects.get(id=pedido).presente

#---------------------------------------------------------------------------------------    


#-------------------------------------DETALLES DE PEDIDO-------------------------------
class DetallePedido(models.Model):
    #id
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    sub_total = models.DecimalField(max_digits=20,decimal_places=2)
    total = models.DecimalField(max_digits=20,decimal_places=2)
#---------------------------------------------------------------------------------------


#------------------------------------NOTIFICACIONES------------------------------------
class Notificaciones(models.Model):
    #id
    autor = models.ForeignKey(Usuario,to_field='username', on_delete=models.CASCADE)
    mensaje = models.TextField()
#---------------------------------------------------------------------------------------    

#------------------------------------CARRITO DE COMPRAS---------------------------------
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
#---------------------------------------------------------------------------------------    
#------------------------------------VENTAS---------------------------------

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    impuesto = models.ForeignKey(Impuesto, on_delete=models.SET_NULL, null=True)  # Añade este campo si es necesario


    def __str__(self):
        return f"Purchase {self.id} by {self.user.username} on {self.created_at}"

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, related_name='purchase_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} de {self.product.descripcion} en la compra {self.purchase.id}"

#---------------------------------------------------------------------------------------    
