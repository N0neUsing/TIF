#renderiza las vistas al usuario
import random
from django.shortcuts import render, redirect, get_object_or_404
# para redirigir a otras paginas
from django.http import Http404, HttpResponseRedirect, HttpResponse,FileResponse
from urllib.parse import quote as urlquote
#el formulario de login
from .forms import *
# clase para crear vistas basadas en sub-clases
from django.views import View
#autentificacion de usuario e inicio de sesion
from django.contrib.auth import authenticate, login, logout
#verifica si el usuario esta logeado
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal, getcontext, ROUND_HALF_UP
from .models import Categoria, Cart, CartItem, Purchase, Impuesto, Cliente, ClienteProducto, PurchaseItem
from .forms import CategoriaForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import PrecioScraping
from django.db.models import Min, Max, Sum, Count
import re
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from django.http import JsonResponse
from django.urls import reverse
import json
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import generics, serializers
from .serializers import CartSerializer, CartItemSerializer
from datetime import date, timedelta
from django.utils import timezone
from urllib.parse import urlparse
import logging
from .models import CartItem
from PIL import Image, ExifTags
import io
from django.core.files.images import ImageFile
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.core.files.base import ContentFile
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
from django.db import transaction
from django.db.models import Max, F, OuterRef, Subquery
from django.utils.timezone import now
from reportlab.lib.pagesizes import landscape
from django.views.decorators.http import require_POST
from rest_framework.views import APIView 
from rest_framework.response import Response
from .serializers import ProductoSerializer
from django.conf import settings
from django.db.models import Q
from unidecode import unidecode
import base64
from statsmodels.tsa.arima.model import ARIMA
import statsmodels.api as sm
import matplotlib.pyplot as plt
import pandas as pd
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt



## S E L E N I U M ---------------------------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException



#modelos
from .models import *
#formularios dinamicos
from django.forms import formset_factory
#funciones personalizadas
from .funciones import *
#Mensajes de formulario
from django.contrib import messages
#Ejecuta un comando en la terminal externa
from django.core.management import call_command
#procesa archivos en .json
from django.core import serializers as core_serializers
#permite acceder de manera mas facil a los ficheros
from django.core.files.storage import FileSystemStorage




#Globales------------------------------------------------------------------------#
def obtener_nombre_dominio(url):
    dominio = urlparse(url).netloc
    if 'www.' in dominio:
        dominio = dominio.replace('www.', '')
    return dominio

logger = logging.getLogger(__name__)


#Fin de vista---------------------------------------------------------------------#        




#Vistas endogenas.

# Parte dedicada al manejo de imagenes--------------------------------------------#
def compress_image(image_path, image_name, quality=50, max_size=(800, 800)):
    image_temporary = Image.open(image_path)
    image_temporary = rotate_image_based_on_exif(image_temporary)
    output_io_stream = BytesIO()
    image_temporary.thumbnail(max_size, Image.Resampling.LANCZOS)
    image_temporary.save(output_io_stream, format='JPEG', quality=quality)
    output_io_stream.seek(0)
    return ContentFile(output_io_stream.read(), name=image_name)


def comprimir_imagenes_productos():
    productos = Producto.objects.all()
    for producto in productos:
        try:
            if producto.imagen_producto:
                nombre_imagen_original = producto.imagen_producto.name
                nombre_imagen_sin_ruta = nombre_imagen_original.split('/')[-1]
                if not nombre_imagen_sin_ruta.startswith('comprimido_'):
                    output_io_stream = compress_image(producto.imagen_producto.path, nombre_imagen_sin_ruta)
                    nuevo_nombre_imagen = f"comprimido_{nombre_imagen_sin_ruta}"
                    producto.imagen_producto.delete(save=False)
                    producto.imagen_producto.save(nuevo_nombre_imagen, File(output_io_stream), save=True)
                    producto.save()
        except FileNotFoundError:
            print(f"El archivo {nombre_imagen_original} no fue encontrado y no se pudo comprimir.")


@receiver(post_delete, sender=Producto)
def eliminar_archivos_producto(sender, instance, **kwargs):
    if instance.imagen_producto:
        instance.imagen_producto.delete(save=False)
    if instance.imagen_codigo_qr:
        instance.imagen_codigo_qr.delete(save=False)

def rotate_image_based_on_exif(image):
    try:
        exif = image._getexif()
        if exif:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break

            if orientation in exif:
                if exif[orientation] == 3:
                    image = image.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    image = image.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass

    return image



#Fin de vista---------------------------------------------------------------------#        

#Interfaz de inicio de sesion-----------------------------------------------------#
class Login(View):
    #Si el usuario ya envio el formulario por metodo post
    def post(self,request):
        # Crea una instancia del formulario y la llena con los datos:
        form = LoginFormulario(request.POST)
        # Revisa si es valido:
        if form.is_valid():
            # Procesa y asigna los datos con form.cleaned_data como se requiere
            usuario = form.cleaned_data['username']
            clave = form.cleaned_data['password']
            # Se verifica que el usuario y su clave existan
            logeado = authenticate(request, username=usuario, password=clave)
            if logeado is not None:
                login(request,logeado)
                #Si el login es correcto lo redirige al panel del sistema:
                return HttpResponseRedirect('/inventario/panel')
            else:
                #De lo contrario lanzara el mismo formulario
                return render(request, 'inventario/login.html', {'form': form})

    # Si se llega por GET crearemos un formulario en blanco
    def get(self,request):
        if request.user.is_authenticated == True:
            return HttpResponseRedirect('/inventario/panel')

        form = LoginFormulario()
        #Envia al usuario el formulario para que lo llene
        return render(request, 'inventario/login.html', {'form': form})
#Fin de vista---------------------------------------------------------------------#        




class Panel(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def get(self, request):
        hoy = timezone.now().date()
        productos_a_vencer = Producto.objects.filter(fecha_vencimiento__lte=hoy + timedelta(days=30)).order_by('-precio')
        productos_incompletos = Producto.objects.filter(models.Q(precio__isnull=True) | models.Q(imagen_producto__isnull=True) | models.Q(tipo__isnull=True))
        productos_bajos_en_stock = Producto.objects.filter(disponible__lt=10).order_by('disponible')

        productos_vendidos = PurchaseItem.objects.filter(purchase__created_at__date=hoy) \
                                                 .values('product__descripcion') \
                                                 .annotate(total_vendido=Sum('quantity'))

        ventas_hoy = Factura.objects.filter(fecha=hoy).order_by('-fecha')
        ventas_recientes = ventas_hoy[:5]  # Solo las 5 más recientes

        clientes = Cliente.objects.all()
        clientes_data = []
        for cliente in clientes:
            productos_cliente = ClienteProducto.objects.filter(cliente=cliente)
            total_sin_impuestos = sum(item.producto.precio * item.cantidad for item in productos_cliente)
            recargo = Decimal('1.10')  # 10% de recargo
            total_con_recargo = total_sin_impuestos * recargo
            if total_con_recargo > 0:
                clientes_data.append({
                    'id': cliente.id,
                    'cedula': cliente.cedula,
                    'nombre': cliente.nombre,
                    'apellido': cliente.apellido,
                    'telefono': cliente.telefono,
                    'totalConRecargo': total_con_recargo,
                })

        # Ventas por horas del día actual
        horas = [f"{str(h).zfill(2)}:00" for h in range(24)]
        totales_horas = [float(Purchase.objects.filter(created_at__date=hoy, created_at__hour=h).aggregate(total=Sum('total'))['total'] or 0) for h in range(24)]

        # Ventas por días de la semana actual
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        start_of_week = hoy - timedelta(days=hoy.weekday())
        totales_dias_semana = [
            float(Purchase.objects.filter(created_at__date=start_of_week + timedelta(days=i)).aggregate(total=Sum('total'))['total'] or 0) for i in range(7)
        ]

        # Ventas por días del mes actual
        dias_mes = [str(d).zfill(2) for d in range(1, hoy.day + 1)]
        totales_dias_mes = [
            float(Purchase.objects.filter(created_at__date=hoy.replace(day=d)).aggregate(total=Sum('total'))['total'] or 0) for d in range(1, hoy.day + 1)
        ]

        # Ventas por meses del año actual
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        totales_meses = [
            float(Purchase.objects.filter(created_at__year=hoy.year, created_at__month=m).aggregate(total=Sum('total'))['total'] or 0) for m in range(1, 13)
        ]

        contexto = {
            'usuario': request.user.username,
            'id_usuario': request.user.id,
            'nombre': request.user.first_name,
            'apellido': request.user.last_name,
            'correo': request.user.email,
            'fecha': hoy,
            'productosRegistrados': Producto.numeroRegistrados(),
            'productosVendidos': productos_vendidos.count(),
            'clientesRegistrados': len(clientes_data),
            'usuariosRegistrados': Usuario.numeroRegistrados(),
            'facturasEmitidas': Factura.numeroRegistrados(),
            'ingresoTotal': Factura.ingresoTotal(),
            'ultimasVentas': DetalleFactura.ultimasVentas(),
            'administradores': Usuario.numeroUsuarios('administrador'),
            'usuarios': Usuario.numeroUsuarios('usuario'),
            'ventasDiarias': Purchase.ventas_diarias(),
            'ventasMensuales': Purchase.ventas_mensuales(),
            'productosAVencer': productos_a_vencer.count(),
            'productosIncompletos': productos_incompletos.count(),
            'productosBajosEnStock': productos_bajos_en_stock.count(),
            'lista_productosAVencer': productos_a_vencer[:5],
            'lista_completa_productosAVencer': productos_a_vencer,
            'lista_productosIncompletos': productos_incompletos,
            'lista_productosBajosEnStock': productos_bajos_en_stock[:5],
            'lista_completa_productosBajosEnStock': productos_bajos_en_stock,
            'lista_productosVendidos': productos_vendidos,
            'lista_completa_productosVendidos': productos_vendidos,
            'lista_clientes': clientes_data[:5],
            'lista_completa_clientes': clientes_data,
            'ventas': ventas_hoy,
            'ventas_recientes': ventas_recientes,
            'ventas_diarias_total': Purchase.ventas_diarias(),
            'ventas_semanales_total': Purchase.ventas_semanales(),
            'ventas_mensuales_total': Purchase.ventas_mensuales(),
            'ventas_anuales_total': Purchase.ventas_anuales(),
            'horas': json.dumps(horas),
            'totales_horas': json.dumps(totales_horas),
            'dias_semana': json.dumps(dias_semana),
            'totales_dias_semana': json.dumps(totales_dias_semana),
            'dias_mes': json.dumps(dias_mes),
            'totales_dias_mes': json.dumps(totales_dias_mes),
            'meses': json.dumps(meses),
            'totales_meses': json.dumps(totales_meses),
        }

        return render(request, 'inventario/panel.html', contexto)



#Maneja la salida del usuario------------------------------------------------------#
class Salir(LoginRequiredMixin, View):
    #Sale de la sesion actual
    login_url = 'inventario/login'
    redirect_field_name = None

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/inventario/login')
#Fin de vista----------------------------------------------------------------------#


#Muestra el perfil del usuario logeado actualmente---------------------------------#
class Perfil(LoginRequiredMixin, View):
    login_url = 'inventario/login'
    redirect_field_name = None

    #se accede al modo adecuado y se valida al usuario actual para ver si puede modificar al otro usuario-
    #-el cual es obtenido por la variable 'p'
    def get(self, request, modo, p):
        if modo == 'editar':
            perf = Usuario.objects.get(id=p)
            editandoSuperAdmin = False

            if p == 1:
                if request.user.nivel != 2:
                    messages.error(request, 'No puede editar el perfil del administrador por no tener los permisos suficientes')
                    return HttpResponseRedirect('/inventario/perfil/ver/%s' % p)
                editandoSuperAdmin = True
            else:
                if request.user.is_superuser != True: 
                    messages.error(request, 'No puede cambiar el perfil por no tener los permisos suficientes')
                    return HttpResponseRedirect('/inventario/perfil/ver/%s' % p) 

                else:
                    if perf.is_superuser == True:
                        if request.user.nivel == 2:
                            pass

                        elif perf.id != request.user.id:
                            messages.error(request, 'No puedes cambiar el perfil de un usuario de tu mismo nivel')

                            return HttpResponseRedirect('/inventario/perfil/ver/%s' % p) 

            if editandoSuperAdmin:
                form = UsuarioFormulario()
                form.fields['level'].disabled = True
            else:
                form = UsuarioFormulario()

            #Me pregunto si habia una manera mas facil de hacer esto, solo necesitaba hacer que el formulario-
            #-apareciera lleno de una vez, pero arrojaba User already exists y no pasaba de form.is_valid()
            form['username'].field.widget.attrs['value']  = perf.username
            form['first_name'].field.widget.attrs['value']  = perf.first_name
            form['last_name'].field.widget.attrs['value']  = perf.last_name
            form['email'].field.widget.attrs['value']  = perf.email
            form['level'].field.widget.attrs['value']  = perf.nivel

            #Envia al usuario el formulario para que lo llene
            contexto = {'form':form,'modo':request.session.get('perfilProcesado'),'editar':'perfil',
            'nombreUsuario':perf.username}

            contexto = complementarContexto(contexto,request.user)
            return render(request,'inventario/perfil/perfil.html', contexto)


        elif modo == 'clave':  
            perf = Usuario.objects.get(id=p)
            if p == 1:
                if request.user.nivel != 2:
                   
                    messages.error(request, 'No puede cambiar la clave del administrador por no tener los permisos suficientes')
                    return HttpResponseRedirect('/inventario/perfil/ver/%s' % p)  
            else:
                if request.user.is_superuser != True: 
                    messages.error(request, 'No puede cambiar la clave de este perfil por no tener los permisos suficientes')
                    return HttpResponseRedirect('/inventario/perfil/ver/%s' % p) 

                else:
                    if perf.is_superuser == True:
                        if request.user.nivel == 2:
                            pass

                        elif perf.id != request.user.id:
                            messages.error(request, 'No puedes cambiar la clave de un usuario de tu mismo nivel')
                            return HttpResponseRedirect('/inventario/perfil/ver/%s' % p) 


            form = ClaveFormulario(request.POST)
            contexto = { 'form':form, 'modo':request.session.get('perfilProcesado'),
            'editar':'clave','nombreUsuario':perf.username }            

            contexto = complementarContexto(contexto,request.user)
            return render(request, 'inventario/perfil/perfil.html', contexto)

        elif modo == 'ver':
            perf = Usuario.objects.get(id=p)
            contexto = { 'perfil':perf }      
            contexto = complementarContexto(contexto,request.user)
          
            return render(request,'inventario/perfil/verPerfil.html', contexto)



    def post(self,request,modo,p):
        if modo ==  'editar':
            # Crea una instancia del formulario y la llena con los datos:
            form = UsuarioFormulario(request.POST)
            # Revisa si es valido:
            
            if form.is_valid():
                perf = Usuario.objects.get(id=p)
                # Procesa y asigna los datos con form.cleaned_data como se requiere
                if p != 1:
                    level = form.cleaned_data['level']        
                    perf.nivel = level
                    perf.is_superuser = level

                username = form.cleaned_data['username']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']

                perf.username = username
                perf.first_name = first_name
                perf.last_name = last_name
                perf.email = email

                perf.save()
                
                form = UsuarioFormulario()
                messages.success(request, 'Actualizado exitosamente el perfil de ID %s.' % p)
                request.session['perfilProcesado'] = True           
                return HttpResponseRedirect("/inventario/perfil/ver/%s" % perf.id)
            else:
                #De lo contrario lanzara el mismo formulario
                return render(request, 'inventario/perfil/perfil.html', {'form': form})

        elif modo == 'clave':
            form = ClaveFormulario(request.POST)

            if form.is_valid():
                error = 0
                clave_nueva = form.cleaned_data['clave_nueva']
                repetir_clave = form.cleaned_data['repetir_clave']
                #clave = form.cleaned_data['clave']

                #Comentare estas lineas de abajo para deshacerme de la necesidad
                #   de obligar a que el usuario coloque la clave nuevamente
                #correcto = authenticate(username=request.user.username , password=clave)


                #if correcto is not None:
                    #if clave_nueva != clave:
                        #pass
                    #else:
                        #error = 1
                        #messages.error(request,"La clave nueva no puede ser identica a la actual") 

                usuario = Usuario.objects.get(id=p) 

                if clave_nueva == repetir_clave:
                    pass
                else:
                    error = 1
                    messages.error(request,"La clave nueva y su repeticion tienen que coincidir")

                #else:
                    #error = 1
                    #messages.error(request,"La clave de acceso actual que ha insertado es incorrecta")

                if(error == 0):
                    messages.success(request, 'La clave se ha cambiado correctamente!')
                    usuario.set_password(clave_nueva)
                    usuario.save()
                    return HttpResponseRedirect("/inventario/login")

                else:
                    return HttpResponseRedirect("/inventario/perfil/clave/%s" % p)
    



  
#----------------------------------------------------------------------------------#   


#Elimina usuarios, productos, clientes o proveedores----------------------------
class Eliminar(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def get(self, request, modo, p):

        if modo == 'producto':
            prod = Producto.objects.get(id=p)
            prod.delete()
            messages.success(request, 'Producto de ID %s borrado exitosamente.' % p)
            return HttpResponseRedirect("/inventario/listarProductos")         
           
        elif modo == 'cliente':
            cliente = Cliente.objects.get(id=p)
            cliente.delete()
            messages.success(request, 'Cliente de ID %s borrado exitosamente.' % p)
            return HttpResponseRedirect("/inventario/listarClientes")            


        elif modo == 'proveedor':
            proveedor = Proveedor.objects.get(id=p)
            proveedor.delete()
            messages.success(request, 'Proveedor de ID %s borrado exitosamente.' % p)
            return HttpResponseRedirect("/inventario/listarProveedores")

        elif modo == 'usuario':
            if request.user.is_superuser == False:
                messages.error(request, 'No tienes permisos suficientes para borrar usuarios')  
                return HttpResponseRedirect('/inventario/listarUsuarios')

            elif p == 1:
                messages.error(request, 'No puedes eliminar al super-administrador.')
                return HttpResponseRedirect('/inventario/listarUsuarios')  

            elif request.user.id == p:
                messages.error(request, 'No puedes eliminar tu propio usuario.')
                return HttpResponseRedirect('/inventario/listarUsuarios')                 

            else:
                usuario = Usuario.objects.get(id=p)
                usuario.delete()
                messages.success(request, 'Usuario de ID %s borrado exitosamente.' % p)
                return HttpResponseRedirect("/inventario/listarUsuarios")        


#Fin de vista-------------------------------------------------------------------   

#
# Parte de Productos------------------------------------------------------------------
#

#Muestra una lista de 10 productos por pagina----------------------------------------#
class ListarProductos(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def get(self, request):
        from django.db import models
        comprimir_imagenes_productos()

        #Lista de productos de la BDD
        productos = Producto.objects.all()
                               
        contexto = {'tabla':productos}

        contexto = complementarContexto(contexto,request.user)  

        return render(request, 'inventario/producto/listarProductos.html',contexto)
#Fin de vista-------------------------------------------------------------------------#



class AgregarProducto(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def get(self, request):
        form = ProductoFormulario()  # Aquí se crea una instancia del formulario
        contexto = {'form': form}
        contexto = complementarContexto(contexto, request.user)
        return render(request, 'inventario/producto/agregarProducto.html', contexto)

    def post(self, request):
        form = ProductoFormulario(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            if 'imagen_producto' in request.FILES:
                imagen_producto = request.FILES['imagen_producto']
                producto.imagen_producto = compress_image(imagen_producto, imagen_producto.name)
            producto.save()
            messages.success(request, 'Producto agregado exitosamente.')
            return HttpResponseRedirect("/inventario/listarProductos")
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
            return render(request, 'inventario/producto/agregarProducto.html', {'form': form})
    





#Formulario simple que procesa un script para importar los productos-----------------#
class ImportarProductos(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def post(self,request):
        form = ImportarProductosFormulario(request.POST)
        if form.is_valid():
            request.session['productosImportados'] = True
            return HttpResponseRedirect("/inventario/importarProductos")

    def get(self,request):
        form = ImportarProductosFormulario()

        if request.session.get('productosImportados') == True:
            importado = request.session.get('productoImportados')
            contexto = { 'form':form,'productosImportados': importado  }
            request.session['productosImportados'] = False

        else:
            contexto = {'form':form}
            contexto = complementarContexto(contexto,request.user) 
        return render(request, 'inventario/producto/importarProductos.html',contexto)        

#Fin de vista-------------------------------------------------------------------------#




#Formulario simple que crea un archivo y respalda los productos-----------------------#
class ExportarProductos(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def post(self,request):
        form = ExportarProductosFormulario(request.POST)
        if form.is_valid():
            request.session['productosExportados'] = True

            #Se obtienen las entradas de producto en formato JSON
            data = serializers.serialize("json", Producto.objects.all())
            fs = FileSystemStorage('inventario/tmp/')

            #Se utiliza la variable fs para acceder a la carpeta con mas facilidad
            with fs.open("productos.json", "w") as out:
                out.write(data)
                out.close()  

            with fs.open("productos.json", "r") as out:                 
                response = HttpResponse(out.read(), content_type="application/force-download")
                response['Content-Disposition'] = 'attachment; filename="productos.json"'
                out.close() 
            #------------------------------------------------------------
            return response

    def get(self,request):
        form = ExportarProductosFormulario()

        if request.session.get('productosExportados') == True:
            exportado = request.session.get('productoExportados')
            contexto = { 'form':form,'productosExportados': exportado  }
            request.session['productosExportados'] = False

        else:
            contexto = {'form':form}
            contexto = complementarContexto(contexto,request.user) 
        return render(request, 'inventario/producto/exportarProductos.html',contexto)
#Fin de vista-------------------------------------------------------------------------#




#Muestra el formulario de un producto especifico para editarlo----------------------------------#
class EditarProducto(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def is_ajax(self, request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    def get(self, request, id):
        producto = get_object_or_404(Producto, pk=id)
        form = ProductoFormulario(instance=producto)
        if self.is_ajax(request):
            return render(request, 'inventario/producto/editar_producto_form.html', {'form': form})
        return render(request, 'inventario/producto/agregarProducto.html', {'form': form, 'editar': True})

    def post(self, request, id):
        producto = get_object_or_404(Producto, pk=id)
        form = ProductoFormulario(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save(commit=False)
            if 'imagen_producto' in request.FILES:
                imagen_producto = request.FILES['imagen_producto']
                imagen_stream = compress_image(imagen_producto, f"comprimido_{imagen_producto.name}")
                imagen_final = InMemoryUploadedFile(
                    imagen_stream,
                    field_name='imagen_producto',
                    name=f"comprimido_{imagen_producto.name}",
                    content_type=imagen_producto.content_type,
                    size=imagen_stream.size,
                    charset=None
                )
                producto.imagen_producto = imagen_final
            producto.save()
            if self.is_ajax(request):
                return JsonResponse({'success': True, 'message': 'Producto actualizado exitosamente.'})
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('inventario:listarProductos')
        else:
            if self.is_ajax(request):
                return JsonResponse({'success': False, 'errors': form.errors})
            return render(request, 'inventario/producto/agregarProducto.html', {'form': form, 'editar': True})


#Fin de vista------------------------------------------------------------------------------------#


#Crea una lista de los clientes, 10 por pagina----------------------------------------#
class ListarClientes(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def get(self, request):
        from django.db import models
        #Saca una lista de todos los clientes de la BDD
        clientes = Cliente.objects.all()                
        contexto = {'tabla': clientes}
        contexto = complementarContexto(contexto,request.user)         

        return render(request, 'inventario/cliente/listarClientes.html',contexto) 
#Fin de vista--------------------------------------------------------------------------#




#Crea y procesa un formulario para agregar a un cliente---------------------------------#
class AgregarCliente(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def post(self, request):
        form = ClienteFormulario(request.POST)
        if form.is_valid():
            # Extrae solo los datos limpios que necesitas
            cedula = form.cleaned_data.get('cedula', '')
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            direccion = form.cleaned_data.get('direccion', '')
            telefono = form.cleaned_data['telefono']
            correo = form.cleaned_data.get('correo', '')

            # Crea y guarda el nuevo cliente
            cliente = Cliente(
                cedula=cedula,
                nombre=nombre,
                apellido=apellido,
                direccion=direccion,
                telefono=telefono,
                correo=correo
            )
            cliente.save()

            messages.success(request, f'Ingresado exitosamente bajo la ID {cliente.id}.')
            request.session['clienteProcesado'] = 'agregado'
            return HttpResponseRedirect("/inventario/agregarCliente")
        else:
            return render(request, 'inventario/cliente/agregarCliente.html', {'form': form})

    def get(self, request):
        form = ClienteFormulario()
        contexto = {'form': form, 'modo': request.session.get('clienteProcesado')}
        return render(request, 'inventario/cliente/agregarCliente.html', contexto)
#Fin de vista-----------------------------------------------------------------------------#        




#Formulario simple que procesa un script para importar los clientes-----------------#
class ImportarClientes(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def post(self,request):
        form = ImportarClientesFormulario(request.POST)
        if form.is_valid():
            request.session['clientesImportados'] = True
            return HttpResponseRedirect("/inventario/importarClientes")

    def get(self,request):
        form = ImportarClientesFormulario()

        if request.session.get('clientesImportados') == True:
            importado = request.session.get('clientesImportados')
            contexto = { 'form':form,'clientesImportados': importado  }
            request.session['clientesImportados'] = False

        else:
            contexto = {'form':form}
            contexto = complementarContexto(contexto,request.user)             
        return render(request, 'inventario/cliente/importarClientes.html',contexto)
#Fin de vista-------------------------------------------------------------------------#




#Formulario simple que crea un archivo y respalda los clientes-----------------------#
class ExportarClientes(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def post(self,request):
        form = ExportarClientesFormulario(request.POST)
        if form.is_valid():
            request.session['clientesExportados'] = True

            #Se obtienen las entradas de producto en formato JSON
            data = serializers.serialize("json", Cliente.objects.all())
            fs = FileSystemStorage('inventario/tmp/')

            #Se utiliza la variable fs para acceder a la carpeta con mas facilidad
            with fs.open("clientes.json", "w") as out:
                out.write(data)
                out.close()  

            with fs.open("clientes.json", "r") as out:                 
                response = HttpResponse(out.read(), content_type="application/force-download")
                response['Content-Disposition'] = 'attachment; filename="clientes.json"'
                out.close() 
            #------------------------------------------------------------
            return response

    def get(self,request):
        form = ExportarClientesFormulario()

        if request.session.get('clientesExportados') == True:
            exportado = request.session.get('clientesExportados')
            contexto = { 'form':form,'clientesExportados': exportado  }
            request.session['clientesExportados'] = False

        else:
            contexto = {'form':form}
            contexto = complementarContexto(contexto,request.user) 
        return render(request, 'inventario/cliente/exportarClientes.html',contexto)
#Fin de vista-------------------------------------------------------------------------#




#Muestra el mismo formulario del cliente pero con los datos a editar----------------------#
class EditarCliente(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def post(self,request,p):
        # Crea una instancia del formulario y la llena con los datos:
        cliente = Cliente.objects.get(id=p)
        form = ClienteFormulario(request.POST, instance=cliente)
        # Revisa si es valido:
    
        if form.is_valid():           
            # Procesa y asigna los datos con form.cleaned_data como se requiere
            cedula = form.cleaned_data['cedula']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            direccion = form.cleaned_data['direccion']
            nacimiento = form.cleaned_data['nacimiento']
            telefono = form.cleaned_data['telefono']
            correo = form.cleaned_data['correo']
            telefono2 = form.cleaned_data['telefono2']
            correo2 = form.cleaned_data['correo2']

            cliente.cedula = cedula
            cliente.nombre = nombre
            cliente.apellido = apellido
            cliente.direccion = direccion
            cliente.nacimiento = nacimiento
            cliente.telefono = telefono
            cliente.correo = correo
            cliente.telefono2 = telefono2
            cliente.correo2 = correo2
            cliente.save()
            form = ClienteFormulario(instance=cliente)

            messages.success(request, 'Actualizado exitosamente el cliente de ID %s.' % p)
            request.session['clienteProcesado'] = 'editado'            
            return HttpResponseRedirect("/inventario/editarCliente/%s" % cliente.id)
        else:
            #De lo contrario lanzara el mismo formulario
            return render(request, 'inventario/cliente/agregarCliente.html', {'form': form})

    def get(self, request,p): 
        cliente = Cliente.objects.get(id=p)
        form = ClienteFormulario(instance=cliente)
        #Envia al usuario el formulario para que lo llene
        contexto = {'form':form , 'modo':request.session.get('clienteProcesado'),'editar':True} 
        contexto = complementarContexto(contexto,request.user)     
        return render(request, 'inventario/cliente/agregarCliente.html', contexto)  
#Fin de vista--------------------------------------------------------------------------------# 


#Emite la primera parte de la factura------------------------------#
class EmitirFactura(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def post(self, request):
        # Crea una instancia del formulario y la llena con los datos:
        cedulas = Cliente.cedulasRegistradas()
        form = EmitirFacturaFormulario(request.POST,cedulas=cedulas)
        # Revisa si es valido:
        if form.is_valid():
            # Procesa y asigna los datos con form.cleaned_data como se requiere
            request.session['form_details'] = form.cleaned_data['productos']
            request.session['id_client'] = form.cleaned_data['cliente']
            return HttpResponseRedirect("detallesDeFactura")
        else:
            #De lo contrario lanzara el mismo formulario
            return render(request, 'inventario/factura/emitirFactura.html', {'form': form})

    def get(self, request):
        cedulas = Cliente.cedulasRegistradas()   
        form = EmitirFacturaFormulario(cedulas=cedulas)
        contexto = {'form':form}
        contexto = complementarContexto(contexto,request.user) 
        return render(request, 'inventario/factura/emitirFactura.html', contexto)
#Fin de vista---------------------------------------------------------------------------------#



#Muestra y procesa los detalles de cada producto de la factura--------------------------------#
class DetallesFactura(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def get(self, request):
        cedula = request.session.get('id_client')
        productos = request.session.get('form_details')
        FacturaFormulario = formset_factory(DetallesFacturaFormulario, extra=productos)
        formset = FacturaFormulario()
        contexto = {'formset':formset}
        contexto = complementarContexto(contexto,request.user) 

        return render(request, 'inventario/factura/detallesFactura.html', contexto)        

    def post(self, request):
        cedula = request.session.get('id_client')
        productos = request.session.get('form_details')

        FacturaFormulario = formset_factory(DetallesFacturaFormulario, extra=productos)

        inicial = {
        'descripcion':'',
        'cantidad': 0,
        'subtotal':0,
        }

        data = {
    'form-TOTAL_FORMS': productos,
    'form-INITIAL_FORMS':0,
    'form-MAX_NUM_FORMS': '',
                }

        formset = FacturaFormulario(request.POST,data)


        if formset.is_valid():

            id_producto = []
            cantidad = []
            subtotal = []
            total_general = []
            sub_monto = 0
            monto_general = 0

            for form in formset:
                desc = form.cleaned_data['descripcion'].descripcion
                cant = form.cleaned_data['cantidad']
                sub = form.cleaned_data['valor_subtotal']
                id_producto.append(obtenerIdProducto(desc)) #esta funcion, a estas alturas, es innecesaria porque ya tienes la id
                cantidad.append(cant)
                subtotal.append(sub)

            #Ingresa la factura
            #--Saca el sub-monto
            for index in subtotal:
                sub_monto += index

            #--Saca el monto general
            for index,element in enumerate(subtotal):
                if productoTieneIva(id_producto[index]):
                    nuevoPrecio = sacarIva(element)   
                    monto_general += nuevoPrecio
                    total_general.append(nuevoPrecio)                     
                else:                   
                    monto_general += element
                    total_general.append(element)        

            from datetime import date

            cliente = Cliente.objects.get(cedula=cedula)
            iva = ivaActual('objeto')
            factura = Factura(cliente=cliente,fecha=date.today(),sub_monto=sub_monto,monto_general=monto_general,iva=iva)

            factura.save()
            id_factura = factura

            for indice,elemento in enumerate(id_producto):
                objetoProducto = obtenerProducto(elemento)
                cantidadDetalle = cantidad[indice]
                subDetalle = subtotal[indice]
                totalDetalle = total_general[indice]

                detalleFactura = DetalleFactura(id_factura=id_factura,id_producto=objetoProducto,cantidad=cantidadDetalle
                    ,sub_total=subDetalle,total=totalDetalle)

                objetoProducto.disponible -= cantidadDetalle
                objetoProducto.save()

                detalleFactura.save()  

            messages.success(request, 'Factura de ID %s insertada exitosamente.' % id_factura.id)
            return HttpResponseRedirect("/inventario/emitirFactura")    
    
#Fin de vista-----------------------------------------------------------------------------------#


#Muestra y procesa los detalles de cada producto de la factura--------------------------------#
class ListarFacturas(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def get(self, request):
        #Lista de productos de la BDD
        facturas = Factura.objects.all()
        #Crea el paginador
                               
        contexto = {'tabla': facturas}
        contexto = complementarContexto(contexto,request.user) 

        return render(request, 'inventario/factura/listarFacturas.html', contexto)        

#Fin de vista---------------------------------------------------------------------------------------#     


#Muestra los detalles individuales de una factura------------------------------------------------#
class VerFactura(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def get(self, request, p):
        factura = Factura.objects.get(id=p)
        detalles = DetalleFactura.objects.filter(id_factura_id=p)
        contexto = {'factura':factura, 'detalles':detalles}
        contexto = complementarContexto(contexto,request.user)     
        return render(request, 'inventario/factura/verFactura.html', contexto)
#Fin de vista--------------------------------------------------------------------------------------#   


#Genera la factura en CSV--------------------------------------------------------------------------#
class GenerarFactura(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def get(self, request, p):
        import csv

        factura = Factura.objects.get(id=p)
        detalles = DetalleFactura.objects.filter(id_factura_id=p) 

        nombre_factura = "factura_%s.csv" % (factura.id)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s"' % nombre_factura
        writer = csv.writer(response)

        writer.writerow(['Producto', 'Cantidad', 'Sub-total', 'Total',
         'Porcentaje IVA utilizado: %s' % (factura.iva.valor_iva)])

        for producto in detalles:            
            writer.writerow([producto.id_producto.descripcion,producto.cantidad,producto.sub_total,producto.total])

        writer.writerow(['Total general:','','', factura.monto_general])

        return response

        #Fin de vista--------------------------------------------------------------------------------------#


#Genera la factura en PDF--------------------------------------------------------------------------#
class GenerarFacturaPDF(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def get(self, request, p):
        import io
        from reportlab.pdfgen import canvas
        import datetime

        factura = Factura.objects.get(id=p)
        general = Opciones.objects.get(id=1)
        detalles = DetalleFactura.objects.filter(id_factura_id=p)          

        data = {
             'fecha': factura.fecha, 
             'monto_general': factura.monto_general,
            'nombre_cliente': factura.cliente.nombre + " " + factura.cliente.apellido,
            'cedula_cliente': factura.cliente.cedula,
            'id_reporte': factura.id,
            'iva': factura.iva.valor_iva,
            'detalles': detalles,
            'modo': 'factura',
            'general':general
        }

        nombre_factura = "factura_%s.pdf" % (factura.id)

        pdf = render_to_pdf('inventario/PDF/prueba.html', data)
        response = HttpResponse(pdf,content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"' % nombre_factura

        return response  

        #Fin de vista--------------------------------------------------------------------------------------#


#Crea una lista de los clientes, 10 por pagina----------------------------------------#
class ListarProveedores(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def get(self, request):
        from django.db import models
        #Saca una lista de todos los clientes de la BDD
        proveedores = Proveedor.objects.all()                
        contexto = {'tabla': proveedores}
        contexto = complementarContexto(contexto,request.user)         

        return render(request, 'inventario/proveedor/listarProveedores.html',contexto) 
#Fin de vista--------------------------------------------------------------------------#




#Crea y procesa un formulario para agregar a un proveedor---------------------------------#
class AgregarProveedor(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def post(self, request):
        # Crea una instancia del formulario y la llena con los datos:
        form = ProveedorFormulario(request.POST)
        # Revisa si es valido:

        if form.is_valid():
            # Procesa y asigna los datos con form.cleaned_data como se requiere

            cedula = form.cleaned_data['cedula']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            direccion = form.cleaned_data['direccion']
            nacimiento = form.cleaned_data['nacimiento']
            telefono = form.cleaned_data['telefono']
            correo = form.cleaned_data['correo']
            telefono2 = form.cleaned_data['telefono2']
            correo2 = form.cleaned_data['correo2']

            proveedor = Proveedor(cedula=cedula,nombre=nombre,apellido=apellido,
                direccion=direccion,nacimiento=nacimiento,telefono=telefono,
                correo=correo,telefono2=telefono2,correo2=correo2)
            proveedor.save()
            form = ProveedorFormulario()

            messages.success(request, 'Ingresado exitosamente bajo la ID %s.' % proveedor.id)
            request.session['proveedorProcesado'] = 'agregado'
            return HttpResponseRedirect("/inventario/agregarProveedor")
        else:
            #De lo contrario lanzara el mismo formulario
            return render(request, 'inventario/proveedor/agregarProveedor.html', {'form': form})        

    def get(self,request):
        form = ProveedorFormulario()
        #Envia al usuario el formulario para que lo llene
        contexto = {'form':form , 'modo':request.session.get('proveedorProcesado')} 
        contexto = complementarContexto(contexto,request.user)         
        return render(request, 'inventario/proveedor/agregarProveedor.html', contexto)
#Fin de vista-----------------------------------------------------------------------------#

#Formulario simple que procesa un script para importar los proveedores-----------------#
class ImportarProveedores(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def post(self,request):
        form = ImportarClientesFormulario(request.POST)
        if form.is_valid():
            request.session['clientesImportados'] = True
            return HttpResponseRedirect("/inventario/importarClientes")

    def get(self,request):
        form = ImportarClientesFormulario()

        if request.session.get('clientesImportados') == True:
            importado = request.session.get('clientesImportados')
            contexto = { 'form':form,'clientesImportados': importado  }
            request.session['clientesImportados'] = False

        else:
            contexto = {'form':form}
            contexto = complementarContexto(contexto,request.user)             
        return render(request, 'inventario/importarClientes.html',contexto)
#Fin de vista-------------------------------------------------------------------------#




#Formulario simple que crea un archivo y respalda los proveedores-----------------------#
class ExportarProveedores(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def post(self,request):
        form = ExportarClientesFormulario(request.POST)
        if form.is_valid():
            request.session['clientesExportados'] = True


            #Se obtienen las entradas de producto en formato JSON
            data = serializers.serialize("json", Cliente.objects.all())
            fs = FileSystemStorage('inventario/tmp/')

            #Se utiliza la variable fs para acceder a la carpeta con mas facilidad
            with fs.open("clientes.json", "w") as out:
                out.write(data)
                out.close()  

            with fs.open("clientes.json", "r") as out:                 
                response = HttpResponse(out.read(), content_type="application/force-download")
                response['Content-Disposition'] = 'attachment; filename="clientes.json"'
                out.close() 
            #------------------------------------------------------------
            return response

    def get(self,request):
        form = ExportarClientesFormulario()

        if request.session.get('clientesExportados') == True:
            exportado = request.session.get('clientesExportados')
            contexto = { 'form':form,'clientesExportados': exportado  }
            request.session['clientesExportados'] = False

        else:
            contexto = {'form':form}
            contexto = complementarContexto(contexto,request.user) 
        return render(request, 'inventario/exportarClientes.html',contexto)
#Fin de vista-------------------------------------------------------------------------#




#Muestra el mismo formulario del cliente pero con los datos a editar----------------------#
class EditarProveedor(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def post(self,request,p):
        # Crea una instancia del formulario y la llena con los datos:
        proveedor = Proveedor.objects.get(id=p)
        form = ProveedorFormulario(request.POST, instance=proveedor)
        # Revisa si es valido:
      
        if form.is_valid():           
            # Procesa y asigna los datos con form.cleaned_data como se requiere
            cedula = form.cleaned_data['cedula']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            direccion = form.cleaned_data['direccion']
            nacimiento = form.cleaned_data['nacimiento']
            telefono = form.cleaned_data['telefono']
            correo = form.cleaned_data['correo']
            telefono2 = form.cleaned_data['telefono2']
            correo2 = form.cleaned_data['correo2']

            proveedor.cedula = cedula
            proveedor.nombre = nombre
            proveedor.apellido = apellido
            proveedor.direccion = direccion
            proveedor.nacimiento = nacimiento
            proveedor.telefono = telefono
            proveedor.correo = correo
            proveedor.telefono2 = telefono2
            proveedor.correo2 = correo2
            proveedor.save()
            form = ProveedorFormulario(instance=proveedor)

            messages.success(request, 'Actualizado exitosamente el proveedor de ID %s.' % p)
            request.session['proveedorProcesado'] = 'editado'            
            return HttpResponseRedirect("/inventario/editarProveedor/%s" % proveedor.id)
        else:
            #De lo contrario lanzara el mismo formulario
            return render(request, 'inventario/proveedor/agregarProveedor.html', {'form': form})

    def get(self, request,p): 
        proveedor = Proveedor.objects.get(id=p)
        form = ProveedorFormulario(instance=proveedor)
        #Envia al usuario el formulario para que lo llene
        contexto = {'form':form , 'modo':request.session.get('proveedorProcesado'),'editar':True} 
        contexto = complementarContexto(contexto,request.user)     
        return render(request, 'inventario/proveedor/agregarProveedor.html', contexto)  
#Fin de vista--------------------------------------------------------------------------------#


#Agrega un pedido-----------------------------------------------------------------------------------#      
class AgregarPedido(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def get(self, request):
        cedulas = Proveedor.cedulasRegistradas()
        form = EmitirPedidoFormulario(cedulas=cedulas)
        contexto = {'form':form}
        contexto = complementarContexto(contexto,request.user) 
        return render(request, 'inventario/pedido/emitirPedido.html', contexto)

    def post(self, request):
        # Crea una instancia del formulario y la llena con los datos:
        cedulas = Proveedor.cedulasRegistradas()
        form = EmitirPedidoFormulario(request.POST,cedulas=cedulas)
        # Revisa si es valido:
        if form.is_valid():
            # Procesa y asigna los datos con form.cleaned_data como se requiere
            request.session['form_details'] = form.cleaned_data['productos']
            request.session['id_proveedor'] = form.cleaned_data['proveedor']
            return HttpResponseRedirect("detallesPedido")
        else:
            #De lo contrario lanzara el mismo formulario
            return render(request, 'inventario/pedido/emitirPedido.html', {'form': form})

#--------------------------------------------------------------------------------------------------#



#Lista todos los pedidos---------------------------------------------------------------------------# 
class ListarPedidos(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def get(self, request):
        from django.db import models
        #Saca una lista de todos los clientes de la BDD
        pedidos = Pedido.objects.all()                
        contexto = {'tabla': pedidos}
        contexto = complementarContexto(contexto,request.user)         

        return render(request, 'inventario/pedido/listarPedidos.html',contexto) 

#------------------------------------------------------------------------------------------------#


#Muestra y procesa los detalles de cada producto de la factura--------------------------------#
class DetallesPedido(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def get(self, request):
        cedula = request.session.get('id_proveedor')
        productos = request.session.get('form_details')
        PedidoFormulario = formset_factory(DetallesPedidoFormulario, extra=productos)
        formset = PedidoFormulario()
        contexto = {'formset':formset}
        contexto = complementarContexto(contexto,request.user) 

        return render(request, 'inventario/pedido/detallesPedido.html', contexto)        

    def post(self, request):
        cedula = request.session.get('id_proveedor')
        productos = request.session.get('form_details')

        PedidoFormulario = formset_factory(DetallesPedidoFormulario, extra=productos)

        inicial = {
        'descripcion':'',
        'cantidad': 0,
        'subtotal':0,
        }

        data = {
    'form-TOTAL_FORMS': productos,
    'form-INITIAL_FORMS':0,
    'form-MAX_NUM_FORMS': '',
                }

        formset = PedidoFormulario(request.POST,data)

 
        if formset.is_valid():

            id_producto = []
            cantidad = []
            subtotal = []
            total_general = []
            sub_monto = 0
            monto_general = 0

            for form in formset:
                desc = form.cleaned_data['descripcion'].descripcion
                cant = form.cleaned_data['cantidad']
                sub = form.cleaned_data['valor_subtotal']
       
                id_producto.append(obtenerIdProducto(desc)) #esta funcion, a estas alturas, es innecesaria porque ya tienes la id
                cantidad.append(cant)
                subtotal.append(sub)        

            #Ingresa la factura
            #--Saca el sub-monto
            for index in subtotal:
                sub_monto += index

            #--Saca el monto general
            for index,element in enumerate(subtotal):
                if productoTieneIva(id_producto[index]):
                    nuevoPrecio = sacarIva(element)   
                    monto_general += nuevoPrecio
                    total_general.append(nuevoPrecio)                     
                else:                   
                    monto_general += element
                    total_general.append(element)        

            from datetime import date

            proveedor = Proveedor.objects.get(cedula=cedula)
            iva = ivaActual('objeto')
            presente = False
            pedido = Pedido(proveedor=proveedor,fecha=date.today(),sub_monto=sub_monto,monto_general=monto_general,iva=iva,
                presente=presente)

            pedido.save()
            id_pedido = pedido

            for indice,elemento in enumerate(id_producto):
                objetoProducto = obtenerProducto(elemento)
                cantidadDetalle = cantidad[indice]
                subDetalle = subtotal[indice]
                totalDetalle = total_general[indice]

                detallePedido = DetallePedido(id_pedido=id_pedido,id_producto=objetoProducto,cantidad=cantidadDetalle
                    ,sub_total=subDetalle,total=totalDetalle)
                detallePedido.save()  


            messages.success(request, 'Pedido de ID %s insertado exitosamente.' % id_pedido.id)
            return HttpResponseRedirect("/inventario/agregarPedido")     
    
#Fin de vista-----------------------------------------------------------------------------------#

#Muestra los detalles individuales de un pedido------------------------------------------------#
class VerPedido(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def get(self, request, p):
        pedido = Pedido.objects.get(id=p)
        detalles = DetallePedido.objects.filter(id_pedido_id=p)
        recibido = Pedido.recibido(p)
        contexto = {'pedido':pedido, 'detalles':detalles,'recibido': recibido}
        contexto = complementarContexto(contexto,request.user)     
        return render(request, 'inventario/pedido/verPedido.html', contexto)
#Fin de vista--------------------------------------------------------------------------------------#   

#Valida un pedido ya insertado------------------------------------------------#
class ValidarPedido(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def get(self, request, p):
        pedido = Pedido.objects.get(id=p)
        detalles = DetallePedido.objects.filter(id_pedido_id=p)

        #Agrega los productos del pedido
        for elemento in detalles:
            elemento.id_producto.disponible += elemento.cantidad
            elemento.id_producto.save()

        pedido.presente = True
        pedido.save()
        messages.success(request, 'Pedido de ID %s verificado exitosamente.' % pedido.id)     
        return HttpResponseRedirect("/inventario/verPedido/%s" % p) 
#Fin de vista--------------------------------------------------------------------------------------#   


#Genera el pedido en CSV--------------------------------------------------------------------------#
class GenerarPedido(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def get(self, request, p):
        import csv

        pedido = Pedido.objects.get(id=p)
        detalles = DetallePedido.objects.filter(id_pedido_id=p) 

        nombre_pedido = "pedido_%s.csv" % (pedido.id)

        response = HttpResponse(content_type='text/csv')

        response['Content-Disposition'] = 'attachment; filename="%s"' % nombre_pedido
        writer = csv.writer(response)

        writer.writerow(['Producto', 'Cantidad', 'Sub-total', 'Total',
         'Porcentaje IVA utilizado: %s' % (pedido.iva.valor_iva)])

        for producto in detalles:            
            writer.writerow([producto.id_producto.descripcion,producto.cantidad,producto.sub_total,producto.total])

        writer.writerow(['Total general:','','', pedido.monto_general])

        return response

        #Fin de vista--------------------------------------------------------------------------------------#




#Genera el pedido en PDF--------------------------------------------------------------------------#
class GenerarPedidoPDF(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def get(self, request, p):

        pedido = Pedido.objects.get(id=p)
        general = Opciones.objects.get(id=1)
        detalles = DetallePedido.objects.filter(id_pedido_id=p)


        data = {
             'fecha': pedido.fecha, 
             'monto_general': pedido.monto_general,
            'nombre_proveedor': pedido.proveedor.nombre + " " + pedido.proveedor.apellido,
            'cedula_proveedor': pedido.proveedor.cedula,
            'id_reporte': pedido.id,
            'iva': pedido.iva.valor_iva,
            'detalles': detalles,
            'modo' : 'pedido',
            'general': general
        }

        nombre_pedido = "pedido_%s.pdf" % (pedido.id)

        pdf = render_to_pdf('inventario/PDF/prueba.html', data)
        response = HttpResponse(pdf,content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"' % nombre_pedido

        return response 
        #Fin de vista--------------------------------------------------------------------------------------#


#Crea un nuevo usuario--------------------------------------------------------------#
class CrearUsuario(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None    

    def get(self, request):
        if request.user.is_superuser:
            form = NuevoUsuarioFormulario()
            #Envia al usuario el formulario para que lo llene
            contexto = {'form':form , 'modo':request.session.get('usuarioCreado')}   
            contexto = complementarContexto(contexto,request.user)  
            return render(request, 'inventario/usuario/crearUsuario.html', contexto)
        else:
            messages.error(request, 'No tiene los permisos para crear un usuario nuevo')
            return HttpResponseRedirect('/inventario/panel')

    def post(self, request):
        form = NuevoUsuarioFormulario(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            rep_password = form.cleaned_data['rep_password']
            level = form.cleaned_data['level']

            error = 0

            if password == rep_password:
                pass

            else:
                error = 1
                messages.error(request, 'La clave y su repeticion tienen que coincidir')

            if usuarioExiste(Usuario,'username',username) is False:
                pass

            else:
                error = 1
                messages.error(request, "El nombre de usuario '%s' ya existe. eliga otro!" % username)


            if usuarioExiste(Usuario,'email',email) is False:
                pass

            else:
                error = 1
                messages.error(request, "El correo '%s' ya existe. eliga otro!" % email)                    

            if(error == 0):
                if level == '0':
                    nuevoUsuario = Usuario.objects.create_user(username=username,password=password,email=email)
                    nivel = 0
                elif level == '1':
                    nuevoUsuario = Usuario.objects.create_superuser(username=username,password=password,email=email)
                    nivel = 1

                nuevoUsuario.first_name = first_name
                nuevoUsuario.last_name = last_name
                nuevoUsuario.nivel = nivel
                nuevoUsuario.save()

                messages.success(request, 'Usuario creado exitosamente')
                return HttpResponseRedirect('/inventario/crearUsuario')

            else:
                return HttpResponseRedirect('/inventario/crearUsuario')
                        
                   



#Fin de vista----------------------------------------------------------------------


#Lista todos los usuarios actuales--------------------------------------------------------------#
class ListarUsuarios(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None    

    def get(self, request):
        usuarios = Usuario.objects.all()
        #Envia al usuario el formulario para que lo llene
        contexto = {'tabla':usuarios}   
        contexto = complementarContexto(contexto,request.user)  
        return render(request, 'inventario/usuario/listarUsuarios.html', contexto)

    def post(self, request):
        pass   

#Fin de vista----------------------------------------------------------------------



#Importa toda la base de datos, primero crea una copia de la actual mientras se procesa la nueva--#
class ImportarBDD(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def get(self, request):
        if request.user.is_superuser == False:
            messages.error(request, 'Solo los administradores pueden importar una nueva base de datos')  
            return HttpResponseRedirect('/inventario/panel')

        form = ImportarBDDFormulario()
        contexto = { 'form': form }
        contexto = complementarContexto(contexto, request.user)
        return render(request, 'inventario/BDD/importar.html', contexto)

    def post(self, request):
        form = ImportarBDDFormulario(request.POST, request.FILES)

        if form.is_valid():
            ruta = 'inventario/archivos/BDD/inventario_respaldo.xml'
            manejarArchivo(request.FILES['archivo'],ruta)

            try:
                call_command('loaddata', ruta, verbosity=0)
                messages.success(request, 'Base de datos subida exitosamente')
                return HttpResponseRedirect('/inventario/importarBDD')
            except Exception:
                messages.error(request, 'El archivo esta corrupto')
                return HttpResponseRedirect('/inventario/importarBDD')





#Fin de vista--------------------------------------------------------------------------------


#Descarga toda la base de datos en un archivo---------------------------------------------#
class DescargarBDD(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def get(self, request):
        #Se obtiene la carpeta donde se va a guardar y despues se crea el respaldo ahi
        fs = FileSystemStorage('inventario/archivos/tmp/')
        with fs.open('inventario_respaldo.xml','w') as output:
            call_command('dumpdata','inventario',indent=4,stdout=output,format='xml', 
                exclude=['contenttypes', 'auth.permission'])

            output.close()

        #Lo de abajo es para descargarlo
        with fs.open('inventario_respaldo.xml','r') as output:
            response = HttpResponse(output.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'attachment; filename="inventario_respaldo.xml"'

            #Cierra el archivo
            output.close()

            #Borra el archivo
            ruta = 'inventario/archivos/tmp/inventario_respaldo.xml'
            call_command('erasefile',ruta)

            #Regresa el archivo a descargar
            return response


#Fin de vista--------------------------------------------------------------------------------


#Configuracion general de varios elementos--------------------------------------------------#
class ConfiguracionGeneral(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def get(self, request):
        conf = Opciones.objects.get(id=1)
        form = OpcionesFormulario()
        
        #Envia al usuario el formulario para que lo llene

        form['moneda'].field.widget.attrs['value']  = conf.moneda
        form['valor_iva'].field.widget.attrs['value']  = conf.valor_iva
        form['mensaje_factura'].field.widget.attrs['value']  = conf.mensaje_factura
        form['nombre_negocio'].field.widget.attrs['value']  = conf.nombre_negocio

        contexto = {'form':form}    
        contexto = complementarContexto(contexto,request.user) 
        return render(request, 'inventario/opciones/configuracion.html', contexto)

    def post(self,request):
        # Crea una instancia del formulario y la llena con los datos:
        form = OpcionesFormulario(request.POST,request.FILES)
        # Revisa si es valido:

        if form.is_valid():
            # Procesa y asigna los datos con form.cleaned_data como se requiere
            moneda = form.cleaned_data['moneda']
            valor_iva = form.cleaned_data['valor_iva']
            mensaje_factura = form.cleaned_data['mensaje_factura']
            nombre_negocio = form.cleaned_data['nombre_negocio']
            imagen = request.FILES.get('imagen',False)

            #Si se subio un logo se sobreescribira en la carpeta ubicada
            #--en la siguiente ruta
            if imagen:
                manejarArchivo(imagen,'inventario/static/inventario/assets/logo/logo2.png')

            conf = Opciones.objects.get(id=1)
            conf.moneda = moneda
            conf.valor_iva = valor_iva
            conf.mensaje_factura = mensaje_factura
            conf.nombre_negocio = nombre_negocio
            conf.save()


            messages.success(request, 'Configuracion actualizada exitosamente!')          
            return HttpResponseRedirect("/inventario/configuracionGeneral")
        else:
            form = OpcionesFormulario(instance=conf)
            #De lo contrario lanzara el mismo formulario
            return render(request, 'inventario/opciones/configuracion.html', {'form': form})

#Fin de vista--------------------------------------------------------------------------------


#Accede a los modulos del manual de usuario---------------------------------------------#
class VerManualDeUsuario(LoginRequiredMixin, View):
    login_url = '/inventario/login'
    redirect_field_name = None

    def get(self, request, pagina):
        if pagina == 'inicio':
            return render(request, 'inventario/manual/index.html') 

        if pagina == 'producto':
            return render(request, 'inventario/manual/producto.html') 

        if pagina == 'proveedor':
            return render(request, 'inventario/manual/proveedor.html') 

        if pagina == 'pedido':
            return render(request, 'inventario/manual/pedido.html') 

        if pagina == 'clientes':
            return render(request, 'inventario/manual/clientes.html') 

        if pagina == 'factura':
            return render(request, 'inventario/manual/factura.html') 

        if pagina == 'usuarios':
            return render(request, 'inventario/manual/usuarios.html')

        if pagina == 'opciones':
            return render(request, 'inventario/manual/opciones.html')



#Fin de vista--------------------------------------------------------------------------------

##
## E S C A N E O -----------------------------------------------------------------------------
##
class EscanearProducto(View):
    def get(self, request):
        # Aquí va la lógica para manejar la solicitud GET
        return render(request, 'inventario/producto/escanear_codigo.html')
    
class ObtenerProductoPorCodigo(View):
    def get(self, request, codigo_barra):
        try:
            producto = Producto.objects.get(codigo_barra=codigo_barra)
            precio = float(producto.precio) if producto.precio is not None else None
            tipo_producto = producto.tipo.nombre if producto.tipo else None  # Se obtiene el nombre del tipo relacionado

            data = {
                'success': True,
                'producto': {
                    'id': producto.id,
                    'descripcion': producto.descripcion,
                    'precio': precio,  # Usar la variable precio que ya tiene la lógica adecuada
                    'tipo': tipo_producto,  # Retorna la representación en string del choice
                    'disponible': producto.disponible,
                    'fecha_vencimiento': producto.fecha_vencimiento.strftime('%Y-%m-%d'),  # Formateado como string
                    'imagen': producto.imagen_producto.url if producto.imagen_producto else None
                }
            }
        except Producto.DoesNotExist:
            data = {
                'success': False,
                'message': 'Producto no encontrado.'
            }
        return JsonResponse(data)



#Fin de vista--------------------------------------------------------------------------------


#Accede a los modulos del manual de usuario---------------------------------------------#
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'inventario/producto/lista.html', {'categorias': categorias})

def crear_categoria(request):
    form = CategoriaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('inventario:lista_categorias')
    return render(request, 'producto/crear_categoria.html', {'form': form})


def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('inventario:lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'inventario/producto/editar_categoria.html', {'form': form, 'categoria': categoria})

def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('inventario:lista_categorias')  # Corregido aquí
    # No necesitas renderizar 'producto/lista.html' aquí si solo estás eliminando.
    return redirect('inventario:lista_categorias')



#Fin de vista--------------------------------------------------------------------------------
    
#Parte dedicada a los precios----------------------------------------------------------------

class PreciosProducto(View):
    
    def get(self, request, *args, **kwargs):
        productos = Producto.objects.all()
        # Cambio importante: remover el argumento buscar_nuevos, asumiendo que por defecto no se buscan nuevos precios.
        precios_context = self.cargar_precios_almacenados(productos)
        return render(request, 'inventario/producto/preciosProducto.html', {'precios_context': precios_context})



    def buscar_precios(self, codigo_barra):
        # Usar las claves API aquí para realizar la búsqueda
        google_api_key = 'AIzaSyBzryp6M5NgaZnLAUOIQ4_KJQNYC-PNNrU'
        google_cse_id = 'e6f1f66c7c2d541f5'
        url = "https://www.googleapis.com/customsearch/v1"
        parametros = {
            'key': google_api_key,
            'cx': google_cse_id,
            'q': f"\"{codigo_barra}\"",
            'cr': 'countryAR',
            'num': 10
        }
        precios_resultados = []
        try:
            respuesta = requests.get(url, params=parametros)
            respuesta.raise_for_status()
            resultados_json = respuesta.json()

            print("Resultados JSON:", resultados_json) #depuracion

            if 'items' in resultados_json:
                for item in resultados_json['items']:
                    resultado_scrape = self.scrape_precio(item['link'], codigo_barra=codigo_barra)
                    if resultado_scrape['precio'] != 'Precio no encontrado' and resultado_scrape['precio'] != 'Error al obtener precio':
                        precios_resultados.append({
                            'url': resultado_scrape['url'],
                            'precio': resultado_scrape['precio']
                        })
            return precios_resultados

        except requests.RequestException as e:
            logger.error(f"Error de solicitud al buscar precios para el código de barra {codigo_barra}: {e}")
        except Exception as e:
            logger.error(f"Error inesperado al buscar precios para el código de barra {codigo_barra}: {e}")
        return precios_resultados
        
        
        
    def cargar_precios_almacenados(self, productos):
        precios_context = []
        for producto in productos:
            precios_almacenados = PrecioScraping.objects.filter(producto=producto).order_by('-fecha_obtencion')
            resultados_busqueda = [{
                'texto_enlace': self.preparar_texto_enlace(precio.fuente),
                'url': precio.fuente,  # La columna debe llamarse fuente en tu modelo
                'precio': precio.precio
            } for precio in precios_almacenados]
            
            if precios_almacenados.exists():
                ultimo_precio = precios_almacenados.first()
                precios_context.append({
                    'producto': producto,
                    'precio_minimo_scraping': ultimo_precio.precio,  # Ajusta según necesidad
                    'precio_maximo_scraping': ultimo_precio.precio,  # Ajusta según necesidad
                    'precio_sugerido': ultimo_precio.precio,  # Ajusta según necesidad
                    'diferencia_precio': 0.0,  # Ajusta según necesidad
                    'ultima_actualizacion': ultimo_precio.fecha_obtencion,
                    'resultados_busqueda': resultados_busqueda
                })
            else:
                precios_context.append({
                    'producto': producto,
                    'precio_minimo_scraping': 0.0,
                    'precio_maximo_scraping': 0.0,
                    'precio_sugerido': 0.0,
                    'diferencia_precio': 0.0,
                    'ultima_actualizacion': 'N/A',
                    'resultados_busqueda': []
                })
        return precios_context

    
    def debe_actualizar(self, producto):
        try:
            ultima_actualizacion = PrecioScraping.objects.filter(producto=producto).latest('fecha_obtencion').fecha_obtencion
            return timezone.now() >= ultima_actualizacion + timedelta(hours=5)
        except PrecioScraping.DoesNotExist:
            return True



    def post(self, request, *args, **kwargs):
        if 'buscar_precios' in request.POST:
            producto_id = request.POST.get('producto_id')
            producto = get_object_or_404(Producto, pk=producto_id)

            if self.debe_actualizar(producto):
                # Obtener y procesar precios desde Google
                resultados_google = self.buscar_precios(producto.codigo_barra)
                self.procesar_y_almacenar_resultados(producto, resultados_google)

                # Obtener y procesar precios desde Pricely
                resultado_pricely = self.scrape_precio_pricely(producto.codigo_barra)
                if resultado_pricely.get('precios'):
                    self.procesar_y_almacenar_resultado_pricely(producto, resultado_pricely)

                # Obtener y procesar precios desde Averiguo
                resultados_averiguo = self.scrape_precio_averiguo(producto.codigo_barra)
                if resultados_averiguo.get('precios'):
                    self.procesar_y_almacenar_precio_averiguo(producto, resultados_averiguo['precios'])

            return redirect('inventario:preciosProducto')
        elif 'actualizar_todos' in request.POST:
            # Aquí podrías tener una lógica para actualizar todos los productos si es necesario
            pass

        # Si no se presionó 'buscar_precios', solo redireccionar
        return redirect('inventario:preciosProducto')





    def actualizar_precios_todos(self, productos):
        for producto in productos:
            if self.debe_actualizar(producto):
                self.actualizar_precios_individual(producto)


    def buscar_y_almacenar_precios_individual(self, producto_id):
        producto = get_object_or_404(Producto, pk=producto_id)
        resultados = self.buscar_precios(producto.codigo_barra)
        logger.info(f"URLs y Precios scrapeados para el producto {producto.descripcion}: {resultados}")

        precios_unicos = set((res['precio'], res['url']) for res in resultados if res['precio'] != 'Precio no encontrado')
        precios = []

        for precio, url in precios_unicos:
            precio_limpio = self.limpiar_precio(precio)
            if precio_limpio is not None and not PrecioScraping.objects.filter(producto=producto, precio=precio_limpio, fuente=url).exists():
                PrecioScraping.objects.create(producto=producto, precio=precio_limpio, fuente=url)
                precios.append(precio_limpio)

        if precios:
            producto.precio_minimo = min(precios)
            producto.precio_maximo = max(precios)
            producto.precio_sugerido = sum(precios) / len(precios)  # Precio sugerido como el promedio
            producto.ultima_actualizacion = timezone.now()
            producto.save()




    def buscar_precios_individual(self, request, producto_id):
        # Obtener el producto específico
        producto = get_object_or_404(Producto, pk=producto_id)
        resultados_busqueda = self.buscar_precios(producto.codigo_barra)
        # Actualizar los precios del producto
        self.actualizar_precios_producto(producto, resultados_busqueda)
        # Redireccionar a la página de precios
        return redirect('inventario:preciosProducto')  # Reemplaza 'inventario:preciosProducto' con el nombre real de tu URL

    def buscar_precios_todos(self, request):
        # Obtener todos los productos
        productos = Producto.objects.all()
        for producto in productos:
            # Verificar si es hora de actualizar el producto
            ultima_actualizacion = producto.precios_scraping.latest('fecha_obtencion').fecha_obtencion if producto.precios_scraping.exists() else timezone.now() - timedelta(hours=5)
            if timezone.now() >= ultima_actualizacion + timedelta(hours=5):
                resultados_busqueda = self.buscar_precios(producto.codigo_barra)
                self.actualizar_precios_producto(producto, resultados_busqueda)
        # Redireccionar a la página de precios
        return redirect('inventario:preciosProducto')

    def actualizar_precios_producto(self, producto, resultados_busqueda):
        precios_validos = []
        for res in resultados_busqueda:
            precio = self.limpiar_precio(res['precio'])
            if precio is not None:
                precios_validos.append(precio)
        
        if precios_validos:
            precio_minimo_scraping = min(precios_validos)
            precio_maximo_scraping = max(precios_validos)
            precio_sugerido = sum(precios_validos) / len(precios_validos)

            # Actualizar o crear un objeto PrecioScraping con los precios encontrados
            PrecioScraping.objects.create(
                producto=producto,
                precio=precio_minimo_scraping,  # Aquí asumimos que quieres guardar el precio mínimo
                fuente='CSE',  # Asumimos una fuente genérica, modifica según sea necesario
            )

            # Actualizar los precios en el objeto Producto
            producto.precio_minimo = precio_minimo_scraping
            producto.precio_maximo = precio_maximo_scraping
            producto.save()

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


    def extraer_precio_json(script_content):
        try:
            # Encontrar el inicio y el final del JSON basado en la función addAndDispatchEvent
            inicio_json = script_content.find('addAndDispatchEvent') + len('addAndDispatchEvent')
            inicio_json = script_content.find('{', inicio_json)
            fin_json = script_content.find('});', inicio_json) + 1

            # Extraer y cargar el JSON
            json_text = script_content[inicio_json:fin_json]
            data = json.loads(json_text)
            precio = data['b']['f']

            return precio
        except Exception as e:
            print(f"Error al extraer precio JSON: {e}")
            return None




    def _buscar_precio_en_clases_comunes(self, soup):
        clases_comunes = ['price', 'product-price', 'sale-price']
        for clase in clases_comunes:
            precio_elemento = soup.find(class_=clase)
            if precio_elemento:
                return precio_elemento.get_text()
        return None
      
         
    def _buscar_precio_en_datos_estructurados(self, soup):
        # Ejemplo suponiendo datos JSON-LD
        script = soup.find('script', type='application/ld+json')
        if script:
            data = json.loads(script.string)
            if 'offers' in data:
                price = data['offers']['price']
                return price
        return None
    
    def _buscar_precio_en_scripts(self, soup, codigo_barra):
        scripts = soup.find_all('script')
        for script in scripts:
            if codigo_barra in script.text:
                matched = re.search(r'Precio: \$([\d\.,]+)', script.text)
                if matched:
                    return matched.group(1)
        return None

        

    def procesar_y_almacenar_resultados(self, producto, resultados_scrapeados):
        # Inicializa las listas de precios
        precios = []
        fuentes = []
        try:
            for resultado in resultados_scrapeados:
                precio_limpiado = self.limpiar_precio(resultado['precio'])
                if precio_limpiado:
                    # Guarda cada precio limpio y su fuente en las listas
                    precios.append(precio_limpiado)
                    fuentes.append(resultado['url'])
                    # Crea un registro de PrecioScraping para cada resultado
                    PrecioScraping.objects.create(
                        producto=producto, 
                        precio=precio_limpiado, 
                        fuente=resultado['url'],
                        fecha_obtencion=timezone.now()
                    )
            # Si hay precios, actualiza el producto con el mínimo, máximo y promedio
            if precios:
                producto.precio_minimo = min(precios)
                producto.precio_maximo = max(precios)
                producto.precio_sugerido = sum(precios) / len(precios)
                producto.ultima_actualizacion = timezone.now()
                producto.save()
            logger.info(f"Resultados procesados y almacenados para el producto {producto.descripcion}")
        except Exception as e:
            logger.error(f"Error al procesar y almacenar resultados para el producto {producto.descripcion}: {e}")


    def actualizar_precios_individual(self, producto):
        try:
            if self.debe_actualizar(producto):
                resultados_scrapeados = self.buscar_precios(producto.codigo_barra)
                if resultados_scrapeados:
                    self.procesar_y_almacenar_resultados(producto, resultados_scrapeados)
                    # Actualizar fecha de última actualización
                    producto.ultima_actualizacion = timezone.now()
                    producto.save()
        except Exception as e:
            logger.error(f"Error al actualizar precios para el producto {producto.descripcion}: {e}")

    

    def procesar_y_almacenar_resultado_pricely(self, producto, resultado_pricely):
        logger.debug(f"Procesando precios de Pricely para {producto.descripcion}")
        today_min = now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_max = now().replace(hour=23, minute=59, second=59, microsecond=999999)

        if resultado_pricely.get('precios'):
            for precio_info in resultado_pricely['precios']:
                precio = precio_info['precio']
                fuente = precio_info['tienda_url']
                logo = precio_info['tienda_logo']  # URL del logotipo

                if isinstance(precio, (int, float)) and precio > 0:
                    exists = PrecioScraping.objects.filter(
                        producto=producto,
                        fuente=fuente,
                        fecha_obtencion__range=(today_min, today_max)
                    ).exists()

                    if not exists:
                        PrecioScraping.objects.create(
                            producto=producto,
                            precio=precio,
                            fuente=fuente,
                            tienda_logo=logo,  # Guardar URL del logo
                            fecha_obtencion=timezone.now()
                        )
                        logger.debug(f"Precio {precio} guardado para {producto.descripcion} con logo {logo}")
                    else:
                        logger.info(f"Precio duplicado no guardado: {precio} para {producto.descripcion} de {fuente}")
                else:
                    logger.warning(f"Precio no válido {precio} encontrado para {producto.descripcion}")
        else:
            logger.warning(f"No se encontraron precios válidos para {producto.descripcion}")




    def scrape_precio_pricely(self, codigo_barra):
        url = f"https://pricely.ar/product/{codigo_barra}"
        driver = None
        try:
            options = Options()
            options.headless = True
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-3.gap-4.mt-4 a"))
            )
            precio_elements = driver.find_elements(By.CSS_SELECTOR, ".grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-3.gap-4.mt-4 a")
            precios_info = []
            
            for elem in precio_elements:
                tienda_nombre = elem.find_element(By.TAG_NAME, 'img').get_attribute('alt')
                tienda_logo = elem.find_element(By.TAG_NAME, 'img').get_attribute('src')
                tienda_url = elem.get_attribute('href')  # Aquí capturamos el enlace correcto
                precio = self.limpiar_precio_pricely(elem.find_element(By.CSS_SELECTOR, '.font-display.text-zinc-700.text-2xl').text)
                
                if precio is not None:
                    precios_info.append({
                        'tienda_nombre': tienda_nombre,
                        'tienda_logo': tienda_logo,
                        'tienda_url': tienda_url,  # Incluimos la URL en la información
                        'precio': precio
                    })

            if precios_info:
                logger.info(f"Precios extraídos para {codigo_barra}: {precios_info}")
                return {'precios': precios_info, 'url': url}
            else:
                logger.warning(f"No se encontraron precios válidos para el producto con código de barra: {codigo_barra}")

        except Exception as e:
            logger.error(f"Error al obtener precios desde {url}: {e}")
        finally:
            if driver:
                driver.quit()
        
        return {'precios': [], 'url': url}


    def limpiar_precio_pricely(self, precio_html):
        try:
            # Eliminar espacios, símbolos de moneda y comas que puedan ser usadas para miles
            precio_texto = re.sub(r'[\s$,]', '', precio_html)

            # Si el precio incluye punto seguido por dos o más ceros, considerarlos como decimales
            if '.' in precio_texto and len(precio_texto.split('.')[1]) > 2:
                # Eliminar el punto y manejarlo como un entero
                precio_texto = precio_texto.replace('.', '')

            # Convertir el texto a entero
            precio_final = int(precio_texto)

            # Ajustar el precio dividiendo por 100 si es demasiado grande
            # Esto es para manejar casos donde el precio ha sido interpretado con dos ceros adicionales
            if precio_final > 100000:  # Asumiendo que no esperas precios superiores a 1000 en formato normal
                precio_final = precio_final / 100

            return int(precio_final)  # Devolver como entero
        except Exception as e:
            logger.error(f"Error al limpiar precio de Pricely: {e}")
            return None

        
    

    def preparar_texto_enlace(self, url):
        dominio = urlparse(url).netloc
        # Elimina 'www.' si está presente, y toma solo la primera parte del dominio
        nombre_legible = dominio.replace('www.', '').split('.')[0]
        return nombre_legible

    def get_precios_recientes():
        # Primero, encuentra la fecha más reciente de obtención de precio para cada producto
        precios_recent_dates = PrecioScraping.objects.filter(
            producto_id=OuterRef('producto_id')
        ).order_by('-fecha_obtencion').values('fecha_obtencion')[:1]

        # Ahora, filtra los precios para obtener solo los más recientes
        precios_recientes = PrecioScraping.objects.annotate(
            fecha_reciente=Subquery(precios_recent_dates)
        ).filter(fecha_obtencion=F('fecha_reciente'))

        return precios_recientes

    def vista_de_precios(request):
        precios = get_precios_recientes()
        # Pasa los precios a tu plantilla
        return render(request, 'inventario/producto/preciosProducto.html', {'precios': precios})


##
## P R E C I O S - A V E R I G U O
##

    def scrape_precio_averiguo(self, codigo_barra):
        url = f"https://averiguo.com.ar/productos?q={codigo_barra}&c=&b="
        driver = None
        try:
            options = Options()
            options.headless = True
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card-body"))
            )

            product_cards = driver.find_elements(By.CSS_SELECTOR, ".card-body")
            precios_info = []

            for card in product_cards:
                try:
                    producto_url = card.find_element(By.CSS_SELECTOR, 'h2 a').get_attribute('href')
                    producto_nombre = card.find_element(By.CSS_SELECTOR, 'h2 a').text
                    precio_texto = card.find_element(By.CSS_SELECTOR, 'div.d-flex.justify-content-between.align-items-center.mt-3 span.text-dark').text
                    tienda_logo = card.find_element(By.CSS_SELECTOR, 'img.avatar.avatar-sm.rounded-circle').get_attribute('src')
                    precio = self.limpiar_precio_averiguo(precio_texto)


                    precios_info.append({
                        'producto_nombre': producto_nombre,
                        'producto_url': f"https://averiguo.com.ar{producto_url}",
                        'precio': precio,
                        'tienda_logo': tienda_logo
                    })
                except NoSuchElementException as e:
                    logging.error(f"Element not found: {e}")
                    continue  # Si alguno de los elementos no se encuentra, continúa con el siguiente

            if precios_info:
                logging.info(f"Precios extraídos para {codigo_barra}: {precios_info}")
                return {'precios': precios_info, 'url': url}
            else:
                logging.warning(f"No se encontraron precios válidos para el producto con código de barra: {codigo_barra}")

        except Exception as e:
            logging.error(f"Error al obtener precios desde {url}: {e}")
        finally:
            if driver:
                driver.quit()

        return {'precios': [], 'url': url}

    
    
    def limpiar_precio_averiguo(self, precio_html):
        try:
            # Asegurarse de que el precio_html es un string
            if not isinstance(precio_html, str):
                precio_html = str(precio_html)

            # Eliminar espacios y símbolos de moneda
            precio_texto = re.sub(r'[\s$]', '', precio_html)

            # Reemplazar comas por puntos si se usa como separador decimal
            precio_texto = precio_texto.replace('.', '')  # Elimina el punto usado para los miles
            precio_texto = precio_texto.replace(',', '.')  # Cambia la coma decimal por un punto

            # Convertir a float y luego a int para obtener el valor entero correcto
            precio_final = int(float(precio_texto))

            # Corrección por si el precio es extremadamente alto
            if precio_final > 100000:
                precio_final /= 100

            return precio_final

        except Exception as e:
            logging.error(f"Error al limpiar precio de Averiguo: {e}")
            return None



    def procesar_y_almacenar_precio_averiguo(self, producto, precios_info):
        today_min = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_max = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        
        for precio_info in precios_info:
            precio = self.limpiar_precio_averiguo(precio_info['precio'])
            fuente = precio_info['producto_url']
            logo = precio_info['tienda_logo']
            
            if precio and precio > 0:
                exists = PrecioScraping.objects.filter(
                    producto=producto,
                    fuente=fuente,
                    fecha_obtencion__range=(today_min, today_max)
                ).exists()
                
                if not exists:
                    PrecioScraping.objects.create(
                        producto=producto,
                        precio=precio,
                        fuente=fuente,
                        tienda_logo=logo,
                        fecha_obtencion=timezone.now()
                    )
                    logger.debug(f"Precio {precio} guardado para {producto.descripcion} con logo {logo}")
                else:
                    logger.info(f"Precio duplicado no guardado: {precio} para {producto.descripcion} de {fuente}")
            else:
                logger.warning(f"Precio no válido {precio} encontrado para {producto.descripcion}")


##
## P R E C I O S -    G O O G L E    S E L E N I U M
##


## A P I   P R E C I O S ##

class PrecioProductoAPI(View):
    def get(self, request, id):
        try:
            producto = Producto.objects.get(pk=id)
            precios = PrecioScraping.objects.filter(producto=producto).order_by('-fecha_obtencion')
            precios_dict = [{
                'precio': precio.precio,
                'fuente': precio.fuente,
                'fecha': precio.fecha_obtencion.strftime('%Y-%m-%d')
            } for precio in precios]
            return JsonResponse({'precios': precios_dict, 'descripcion': producto.descripcion}, safe=False)
        except Producto.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)



#Fin de vista--------------------------------------------------------------------------------

#Carrito de compras--------------------------------------------------------------------------


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Producto, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 0}
        )

        if cart_item.quantity + 1 > product.disponible:
            return JsonResponse({'success': False, 'message': f"No puedes agregar más de {product.disponible} unidades de {product.descripcion}."})
        
        cart_item.quantity += 1
        cart_item.save()

        return JsonResponse({'success': True, 'message': f'Producto {product.descripcion} agregado correctamente.'})



class CartView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        products = []
        total = 0
        impuestos = Impuesto.objects.all()
        for product_id, quantity in cart.items():
            product = get_object_or_404(Producto, id=product_id)
            precio = float(product.precio)
            total += precio * int(quantity)
            products.append({'product': product, 'quantity': quantity})
        return render(request, 'inventario/producto/carrito.html', {'products': products, 'total': total, 'impuestos': impuestos})
    
        
class UpdateCartItemView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body.decode('utf-8'))
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'Usuario no autenticado.'}, status=401)

        product_id = kwargs.get('product_id')
        desired_price = body.get('desired_price')
        quantity = body.get('quantity')

        try:
            cart_item = get_object_or_404(CartItem, product_id=product_id, cart__user=request.user)
            product = cart_item.product

            if desired_price is not None and product.precio_por_gramo:
                quantity = float(desired_price) / product.precio_por_gramo
                cart_item.quantity = quantity

            if quantity is not None:
                cart_item.quantity = int(quantity)

            if product.precio is None:
                return JsonResponse({'success': False, 'message': 'Precio del producto no disponible.'}, status=400)

            cart_item.save()
            new_subtotal = cart_item.quantity * product.precio
            total_sin_impuestos = sum(item.quantity * item.product.precio for item in CartItem.objects.filter(cart=cart_item.cart))
            impuesto_id = request.GET.get('impuesto_id')
            if impuesto_id:
                impuesto = get_object_or_404(Impuesto, id=impuesto_id)
                total_con_impuestos = total_sin_impuestos * (1 + impuesto.porcentaje / 100)
            else:
                total_con_impuestos = total_sin_impuestos

            return JsonResponse({
                'success': True,
                'message': 'Carrito actualizado.',
                'new_subtotal': new_subtotal,
                'total_con_impuestos': total_con_impuestos
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al actualizar el carrito: {str(e)}'}, status=500)



class RemoveFromCartView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        try:
            cart = get_object_or_404(Cart, user=request.user)
            cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
            cart_item.delete()
            return JsonResponse({'success': True, 'message': 'Producto eliminado del carrito.'})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Producto no encontrado en el carrito.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)




class Checkout(View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items:
            messages.info(request, "Tu carrito está vacío.")
            return redirect('inventario/producto/carrito.html')
        context = {
            'cart_items': cart_items,
            'total': sum(item.product.precio * item.quantity for item in cart_items)
        }
        return render(request, 'inventario/producto/carrito.html', context)

    def post(self, request):
        impuesto_id = request.POST.get('impuesto_id')
        impuesto = get_object_or_404(Impuesto, id=impuesto_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items:
            messages.error(request, "Tu carrito está vacío.")
            return redirect('inventario/producto/carrito.html')

        pdf_buffer = BytesIO()
        page_width = 164  # Ancho en puntos para 58 mm
        page_height = 800  # Altura suficiente para el contenido del recibo
        p = canvas.Canvas(pdf_buffer, pagesize=(page_width, page_height))
        p.setFont("Helvetica", 8)

        y = page_height - 20  # Comenzar desde un margen pequeño
        y = self.draw_wrapped_text(p, "4 Ases - Comprobante de Compra", 10, y, page_width - 20)

        total_sin_impuestos = 0
        for item in cart_items:
            if item.quantity > item.product.disponible:
                messages.error(request, f"No hay suficiente stock para {item.product.descripcion}.")
                return redirect('inventario:cart')
            if item.product.precio is None:
                messages.error(request, f"El producto {item.product.descripcion} no tiene un precio definido.")
                return redirect('inventario:cart')
            
            subtotal = item.quantity * item.product.precio
            total_sin_impuestos += subtotal

            # Asumimos que el campo 'tipo' del producto tiene un atributo 'nombre' que indica la unidad de venta
            quantity_display = f"{item.quantity} {item.product.tipo.nombre}"
            item_description = f"{item.product.descripcion}: {quantity_display} x ${item.product.precio:.2f} = ${subtotal:.2f}"
            y = self.draw_wrapped_text(p, item_description, 10, y - 10, page_width - 20)

        total_con_impuestos = total_sin_impuestos * (1 + impuesto.tasa / 100)
        y = self.draw_wrapped_text(p, "----------------------------------", 10, y - 10, page_width - 20)
        y = self.draw_wrapped_text(p, f"Total: ${total_con_impuestos:.2f}", 10, y - 10, page_width - 20)
        y = self.draw_wrapped_text(p, f"Fecha de Emisión: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}", 10, y - 10, page_width - 20)
        self.draw_wrapped_text(p, "Gracias por Comprar en 4 Ases", 10, y - 30, page_width - 20)
        y = self.draw_wrapped_text(p, "                                  ", 10, y - 10, page_width - 20)
        y = self.draw_wrapped_text(p, "                                  ", 10, y - 10, page_width - 20)

        p.showPage()
        p.save()
        pdf_buffer.seek(0)

        purchase = Purchase.objects.create(user=request.user, total=total_con_impuestos)
        for item in cart_items:
            PurchaseItem.objects.create(
                purchase=purchase,
                product=item.product,
                quantity=item.quantity,
                price=item.product.precio
            )
        cart_items.delete()

        purchase_id = purchase.id
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="recibo_{purchase_id}.pdf"'
        return response

    def draw_wrapped_text(self, p, text, x, y, max_width):
        # Esta función dibuja texto en el canvas y devuelve la coordenada y actualizada
        words = text.split()
        current_line = ""
        space_width = p.stringWidth(' ', "Helvetica", 8)
        for word in words:
            word_width = p.stringWidth(word, "Helvetica", 8)
            if p.stringWidth(current_line + word, "Helvetica", 8) + space_width > max_width:
                p.drawString(x, y, current_line)
                y -= 10
                current_line = word + ' '
            else:
                current_line += word + ' '
        if current_line:
            p.drawString(x, y, current_line)
        return y


class UpdateProductPriceView(View):
    def post(self, request, product_id):
        try:
            data = json.loads(request.body)
            nuevo_precio = data.get('precio')  # Cambio aquí para esperar 'precio' en lugar de 'price'
            if nuevo_precio is None:
                return JsonResponse({'success': False, 'message': 'Precio no proporcionado'}, status=400)

            product = get_object_or_404(Producto, id=product_id)
            product.precio = float(nuevo_precio)  # Asegúrate de que es un número flotante válido
            product.save()
            return JsonResponse({'success': True, 'message': 'Precio actualizado correctamente.'})
        except Exception as e:
            print(f"Error al actualizar el precio: {str(e)}")
            return JsonResponse({'success': False, 'message': str(e)}, status=500)


def buscar_productos(request):
    query = unidecode(request.GET.get('q', '').lower())  # Convertir el query a minúsculas y eliminar acentos

    # Normalizar las descripciones y los códigos de barra en la consulta
    productos = Producto.objects.all()
    productos = [producto for producto in productos if 
                 unidecode(producto.descripcion.lower()).find(query) != -1 or 
                 unidecode(producto.codigo_barra.lower()).find(query) != -1]

    results = [{
        'id': producto.id,
        'text': producto.descripcion,
        'codigo_barra': producto.codigo_barra,
        'precio': float(producto.precio) if producto.precio else None,
        'cantidad': producto.disponible if producto.disponible is not None else 0,
        'imagen_url': producto.imagen_producto.url if producto.imagen_producto else '/path/to/default/image.png'
    } for producto in productos]

    print(results)  # Esto mostrará los resultados en la consola del servidor
    return JsonResponse({'results': results})





def generate_pdf_receipt(cart):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "Recibo de Compra")

    y = 700
    p.setFont("Helvetica", 12)
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Producto, id=product_id)
        line_total = float(product.precio) * int(quantity)
        total += line_total
        p.drawString(100, y, f"{product.descripcion} x {quantity} @ ${product.precio} cada uno: ${line_total:.2f}")
        y -= 20

    p.drawString(100, y, f"Total: ${total:.2f}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

class AgregarProductoPorCodigo(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        codigo_barra = data.get('codigoBarra')
        producto = get_object_or_404(Producto, codigo_barra=codigo_barra)

        cart, created = Cart.objects.get_or_create(user=request.user, defaults={})
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=producto,
            defaults={'quantity': 0})

        if cart_item.quantity + 1 > producto.disponible:
            return JsonResponse({'success': False, 'message': f"No puedes agregar más de {producto.disponible} unidades de {producto.descripcion}."})

        cart_item.quantity += 1
        cart_item.save()

        return JsonResponse({
            'success': True,
            'message': f'Producto {producto.descripcion} agregado correctamente.',
            'producto': {
                'id': producto.id,
                'descripcion': producto.descripcion,
                'precio': producto.precio,
                'imagen': producto.imagen_producto.url if producto.imagen_producto else None
            }
        })
    

class TotalConImpuestosView(LoginRequiredMixin, View):
    def get(self, request):
        impuesto_id = request.GET.get('impuesto_id')
        impuesto = get_object_or_404(Impuesto, id=impuesto_id)
        cart = get_object_or_404(Cart, user=request.user)

        total_sin_impuestos = sum(item.product.precio * item.quantity for item in cart.items.all())
        total_con_impuestos = total_sin_impuestos * (1 + impuesto.tasa / 100)

        # Agregar registros para depuración
        print(f"Total sin impuestos: {total_sin_impuestos}")
        print(f"Impuesto aplicado: {impuesto.tasa}")
        print(f"Total con impuestos: {total_con_impuestos}")

        return JsonResponse({'total_con_impuestos': float(total_con_impuestos)})

#---------API para carrito-----------------------------------------------------------------------------
class GetCartItemsView(LoginRequiredMixin, generics.ListAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        """
        Este método devuelve los ítems del carrito para el usuario actual.
        """
        user = self.request.user
        cart, _ = Cart.objects.get_or_create(user=user, defaults={})
        return CartItem.objects.filter(cart=cart)


class CartItemSerializer(serializers.ModelSerializer):
    imagen_producto_url = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'imagen_producto_url']
    
    def get_imagen_producto_url(self, obj):
        request = self.context.get('request')
        if obj.product.imagen_producto and hasattr(obj.product.imagen_producto, 'url'):
            return request.build_absolute_uri(obj.product.imagen_producto.url)
        return None

    def get_serializer_context(self):
        """
        Asegúrate de incluir el request en el contexto del serializador para construir URLs completas.
        """
        return {'request': self.request}


class CartListCreateAPIView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemCreateAPIView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get(self, request, *args, **kwargs):
        # Asume que un carrito ya existe. Considera manejar el caso donde el carrito no exista.
        cart, _ = Cart.objects.get_or_create(user=request.user, defaults={})
        cart_items = CartItem.objects.filter(cart=cart)


        items = []
        for item in cart_items:
            # Construye la URL de la imagen si existe, de lo contrario, usa None
            imagen_producto_url = None
            if item.product.imagen_producto:
                imagen_producto_url = request.build_absolute_uri(settings.MEDIA_URL + urlquote(item.product.imagen_producto.name))
            
            # Agrega la información del producto al listado de items
            items.append({
                'id': item.product.id,
                'descripcion': item.product.descripcion,
                'precio': item.product.precio,
                'cantidad': item.quantity,
                'subtotal': item.quantity * item.product.precio,
                'imagen_producto': imagen_producto_url
            })
        
        total = sum(item['subtotal'] for item in items)
        
        return JsonResponse({'items': items, 'total': total})



#Fin de vista--------------------------------------------------------------------------------

#  I M P U E S T O S --------------------------------------------------------------------------


class ListarImpuestos(View):
    def get(self, request):
        impuestos = list(Impuesto.objects.values())
        return JsonResponse(impuestos, safe=False)


class CrearImpuesto(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            impuesto = Impuesto.objects.create(nombre=data['nombre'], tasa=data['tasa'])
            return JsonResponse({'status': 'Impuesto creado', 'id': impuesto.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class EditarImpuesto(View):
    def put(self, request, id):
        try:
            data = json.loads(request.body)
            impuesto = Impuesto.objects.get(id=id)
            impuesto.nombre = data['nombre']
            impuesto.tasa = data['tasa']
            impuesto.save()
            return JsonResponse({'status': 'Impuesto actualizado'}, status=200)
        except Impuesto.DoesNotExist:
            return JsonResponse({'error': 'Impuesto no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class EliminarImpuesto(View):
    def delete(self, request, id):
        try:
            impuesto = Impuesto.objects.get(id=id)
            impuesto.delete()
            return JsonResponse({'status': 'Impuesto eliminado'}, status=204)
        except Impuesto.DoesNotExist:
            return JsonResponse({'error': 'Impuesto no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


#Fin de vista--------------------------------------------------------------------------------

#  V E N T A S ------------------------------------------------------------------------------

class VentasView(View):
    def get(self, request):
        ventas = Purchase.objects.prefetch_related('purchase_items').all().order_by('-created_at')
        
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        total_min = request.GET.get('total_min')
        total_max = request.GET.get('total_max')

        if fecha_inicio:
            ventas = ventas.filter(created_at__date__gte=fecha_inicio)
        if fecha_fin:
            ventas = ventas.filter(created_at__date__lte=fecha_fin)
        if total_min:
            ventas = ventas.filter(total__gte=total_min)
        if total_max:
            ventas = ventas.filter(total__lte=total_max)
        
        detalles_ventas = [
            {
                'venta_id': venta.id,
                'fecha': venta.created_at.strftime('%Y-%m-%d'),
                'total': venta.total,
                'productos': [
                    {
                        'producto_id': purchase_item.product.id,
                        'descripcion': purchase_item.product.descripcion,
                        'precio_unitario': purchase_item.price,
                        'cantidad': purchase_item.quantity,
                        'precio_total': purchase_item.quantity * purchase_item.price,
                    } 
                    for purchase_item in venta.purchase_items.all()
                ]
            } for venta in ventas
        ]
        
        return render(request, 'inventario/ventas/listar_ventas.html', {'ventas': detalles_ventas})

class EliminarVentaView(View):
    def post(self, request):
        venta_id = request.POST.get('venta_id')
        venta = get_object_or_404(Purchase, id=venta_id)
        venta.delete()
        messages.success(request, 'Venta eliminada correctamente.')
        return redirect('inventario:listar_ventas')

class ImprimirTicketView(View):
    def get(self, request, venta_id):
        venta = get_object_or_404(Purchase, id=venta_id)
        venta_items = PurchaseItem.objects.filter(purchase=venta)

        pdf_buffer = BytesIO()
        page_width = 164  # Ancho en puntos para 58 mm
        page_height = 800  # Altura suficiente para el contenido del recibo
        p = canvas.Canvas(pdf_buffer, pagesize=(page_width, page_height))
        p.setFont("Helvetica", 8)

        y = page_height - 20  # Comenzar desde un margen pequeño
        y = self.draw_wrapped_text(p, "4 Ases - Comprobante de Compra", 10, y, page_width - 20)

        total_sin_impuestos = 0
        for item in venta_items:
            subtotal = item.quantity * item.price
            total_sin_impuestos += subtotal

            # Asumimos que el campo 'tipo' del producto tiene un atributo 'nombre' que indica la unidad de venta
            quantity_display = f"{item.quantity} {item.product.tipo.nombre}"
            item_description = f"{item.product.descripcion}: {quantity_display} x ${item.price:.2f} = ${subtotal:.2f}"
            y = self.draw_wrapped_text(p, item_description, 10, y - 10, page_width - 20)

        y = self.draw_wrapped_text(p, "----------------------------------", 10, y - 10, page_width - 20)
        y = self.draw_wrapped_text(p, f"Total: ${venta.total:.2f}", 10, y - 10, page_width - 20)
        y = self.draw_wrapped_text(p, f"Fecha de Emisión: {venta.created_at.strftime('%Y-%m-%d %H:%M:%S')}", 10, y - 10, page_width - 20)
        self.draw_wrapped_text(p, "Gracias por Comprar en 4 Ases", 10, y - 30, page_width - 20)
        y = self.draw_wrapped_text(p, "                                  ", 10, y - 10, page_width - 20)
        y = self.draw_wrapped_text(p, "                                  ", 10, y - 10, page_width - 20)

        p.showPage()
        p.save()
        pdf_buffer.seek(0)

        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="ticket_{venta_id}.pdf"'
        return response

    def draw_wrapped_text(self, p, text, x, y, max_width):
        words = text.split()
        current_line = ""
        space_width = p.stringWidth(' ', "Helvetica", 8)
        for word in words:
            word_width = p.stringWidth(word, "Helvetica", 8)
            if p.stringWidth(current_line + word, "Helvetica", 8) + space_width > max_width:
                p.drawString(x, y, current_line)
                y -= 10
                current_line = word + ' '
            else:
                current_line += word + ' '
        if current_line:
            p.drawString(x, y, current_line)
        return y

def ventas_avanzadas(request):
    # Obtener todas las compras y detalles de los productos vendidos
    compras = Purchase.objects.all().values('created_at', 'total')
    items = PurchaseItem.objects.all().values('purchase__created_at', 'product__descripcion', 'quantity', 'price')

    # Convertir a DataFrame de pandas
    df_compras = pd.DataFrame(list(compras))
    df_items = pd.DataFrame(list(items))

    df_compras['created_at'] = pd.to_datetime(df_compras['created_at'])
    df_items['purchase__created_at'] = pd.to_datetime(df_items['purchase__created_at'])

    # Agrupar por día y sumar las ventas
    ventas_por_dia = df_compras.groupby(df_compras['created_at'].dt.date)['total'].sum()

    # Agrupar por día y producto
    ventas_por_producto_dia = df_items.groupby([df_items['purchase__created_at'].dt.date, 'product__descripcion'])['quantity'].sum().unstack(fill_value=0)

    # Asegurarse de que los datos no contengan NaN y sean del tipo correcto
    ventas_por_dia = ventas_por_dia.astype(float).dropna()

    # Gráfico de ventas diarias
    fig, ax = plt.subplots()
    ax.plot(ventas_por_dia.index, ventas_por_dia.values, marker='o')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Ventas')
    ax.set_title('Ventas Diarias')
    plt.xticks(rotation=45)
    
    # Guardar el gráfico en un buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    # Convertir a base64
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # Predicciones
    model = ARIMA(ventas_por_dia.values, order=(5,1,0))
    model_fit = model.fit()
    pred = model_fit.forecast(steps=30)
    
    contexto = {
        'ventas_por_dia': ventas_por_dia,
        'dia_con_mas_ventas': ventas_por_dia.idxmax(),
        'media_ventas_diarias': ventas_por_dia.mean(),
        'desviacion_ventas_diarias': ventas_por_dia.std(),
        'predicciones': pred,
        'graphic': graphic,
        'ventas_por_producto_dia': ventas_por_producto_dia
    }

    return render(request, 'inventario/ventas/ventas_avanzadas.html', contexto)

class FiltrarIngresosView(View):
    def get(self, request):
        # Lógica para filtrar ingresos
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        total_min = request.GET.get('total_min')
        total_max = request.GET.get('total_max')
        
        facturas = Factura.objects.all()
        
        if fecha_inicio:
            facturas = facturas.filter(fecha__gte=fecha_inicio)
        if fecha_fin:
            facturas = facturas.filter(fecha__lte=fecha_fin)
        if total_min:
            facturas = facturas.filter(monto_general__gte=total_min)
        if total_max:
            facturas = facturas.filter(monto_general__lte=total_max)
        
        contexto = {
            'facturas': facturas
        }
        
        return render(request, 'inventario/filtrar_ingresos.html', contexto)




# Fin de vista--------------------------------------------------------------------------------

##
## C L I E N T E S 
##

class AssignCartToClientView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))  # Decodifica y parsea el JSON
            cliente_id = data.get('cliente_id')
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

        if not cliente_id:
            return JsonResponse({'success': False, 'message': "No se especificó un cliente."}, status=400)

        cliente = get_object_or_404(Cliente, pk=cliente_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return JsonResponse({'success': False, 'message': "No hay productos en el carrito."}, status=400)

        for item in cart_items:
            ClienteProducto.objects.create(
                cliente=cliente,
                producto=item.product,
                cantidad=item.quantity
            )
            item.product.disponible -= item.quantity
            item.product.save()

        cart_items.delete()

        return JsonResponse({'success': True, 'message': f"Productos asignados exitosamente a {cliente.nombre} {cliente.apellido}."})


    
class ApiClientes(APIView):
    def get(self, request, *args, **kwargs):
        clientes = Cliente.objects.all().values('id', 'nombre', 'apellido')
        return Response(list(clientes))
    

def get_cliente_productos(request, cliente_id):
    # Asumiendo que ClienteProducto tiene una FK 'producto' a Producto
    cliente_productos = ClienteProducto.objects.filter(cliente_id=cliente_id).select_related('producto')
    serializer = ProductoSerializer([cp.producto for cp in cliente_productos], many=True, context={'request': request})
    return JsonResponse(serializer.data, safe=False)




class ClientProductsView(View):
    print("se llamo a la funcion")
    def get(self, request, client_id):
        try:
            cliente = Cliente.objects.get(pk=client_id)
            # Aseguramos la carga eficiente de los datos relacionados del producto
            productos_cliente = ClienteProducto.objects.filter(cliente=cliente).select_related('producto')
            productos_data = [
                {
                    'descripcion': pc.producto.descripcion,
                    'cantidad': pc.cantidad,
                    'precio': float(pc.producto.precio)  # Asegúrate de que el modelo Producto tiene un campo 'precio'
                }
                for pc in productos_cliente
            ]
            return JsonResponse(productos_data, safe=False)
        except Cliente.DoesNotExist:
            return JsonResponse({'error': 'Cliente no encontrado'}, status=404)


        
class ClienteProductosAPIView(APIView):
    def get(self, request, cliente_id):
        cliente_productos = ClienteProducto.objects.filter(cliente_id=cliente_id).select_related('producto')
        productos = [cp.producto for cp in cliente_productos]
        print("Productos antes de serializar:", productos)
        for producto in productos:
            print("Producto:", producto.descripcion, "Precio:", producto.precio)
        serializer = ProductoSerializer(productos, many=True, context={'request': request})
        data = serializer.data
        print("Datos serializados:", data)
        return Response(data)




        
class PagarCuentaClienteView(View):
    def post(self, request, cliente_id):
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        productos_cliente = ClienteProducto.objects.filter(cliente=cliente)

        if not productos_cliente.exists():
            messages.error(request, "No hay productos registrados en la cuenta de este cliente.")
            return redirect('ruta_a_listar_clientes')

        pdf_buffer = BytesIO()
        page_width = 164  # Ancho en puntos para 58 mm
        page_height = 800  # Altura inicial de la página
        p = canvas.Canvas(pdf_buffer, pagesize=(page_width, page_height))
        p.setFont("Helvetica", 8)

        y = page_height - 20  # Comenzar desde un margen pequeño
        y = self.draw_wrapped_text(p, "4 Ases - Recibo de Pago de Cuenta", 10, y, page_width - 20)

        total_sin_impuestos = sum(item.producto.precio * item.cantidad for item in productos_cliente)
        recargo = Decimal('1.10')  # Usa Decimal para definir el porcentaje de recargo
        total_con_recargo = total_sin_impuestos * recargo  # Ahora ambos son Decimals

        for item in productos_cliente:
            line = f"{item.producto.descripcion}: {item.cantidad} x ${item.producto.precio:.2f} = ${item.producto.precio * Decimal(item.cantidad):.2f}"
            y = self.draw_wrapped_text(p, line, 10, y - 10, page_width - 20)
            if y < 40:  # Si la posición y está cerca del final de la página, crear una nueva página
                p.showPage()
                p.setFont("Helvetica", 8)
                y = page_height - 20  # Reiniciar y para la nueva página

        y = self.draw_wrapped_text(p, "----------------------------------", 10, y - 10, page_width - 20)
        y = self.draw_wrapped_text(p, f"Total sin impuestos: ${total_sin_impuestos:.2f}", 10, y - 10, page_width - 20)
        y = self.draw_wrapped_text(p, f"Precio por pago con cuenta (10% adicional): ${total_con_recargo:.2f}", 10, y - 10, page_width - 20)
        y = self.draw_wrapped_text(p, f"Fecha de emisión: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}", 10, y - 10, page_width - 20)
        self.draw_wrapped_text(p, "Gracias por Comprar en 4 Ases", 10, y - 30, page_width - 20)

        p.showPage()
        p.save()
        pdf_buffer.seek(0)

        productos_cliente.delete()  # Eliminar productos tras pagar

        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="recibo_pago_cuenta_{cliente_id}.pdf"'
        return response

    def draw_wrapped_text(self, p, text, x, y, max_width):
        words = text.split()
        current_line = ""
        space_width = p.stringWidth(' ', "Helvetica", 8)
        line_height = 10  # Altura de línea para separar adecuadamente las líneas de texto

        for word in words:
            if p.stringWidth(current_line + word, "Helvetica", 8) + space_width > max_width:
                p.drawString(x, y, current_line)
                y -= line_height  # Mueve 'y' hacia abajo para la siguiente línea
                current_line = word + ' '
            else:
                current_line += word + ' '
        if current_line:  # Dibuja la última línea si queda alguna
            p.drawString(x, y, current_line)
            y -= line_height  # Ajusta 'y' después de la última línea

        return y  # Retorna la nueva posición de 'y' para continuar dibujando más abajo







#Fin de vista--------------------------------------------------------------------------------
