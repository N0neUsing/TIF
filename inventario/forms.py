from django import forms
from .models import Producto,Cliente, Proveedor, Usuario, Opciones, Categoria, TipoProducto, Impuesto
from django.utils import timezone

from django.forms import ModelChoiceField

class MisProductos(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.descripcion

class MisPrecios(ModelChoiceField):
    def label_from_instance(self,obj):
        return "%s" % obj.precio

class MisDisponibles(ModelChoiceField):
    def label_from_instance(self,obj):
        return "%s" % obj.disponible


class LoginFormulario(forms.Form):
    username = forms.CharField(label="Tu nombre de usuario",widget=forms.TextInput(attrs={'placeholder': 'Tu nombre de usuario',
        'class': 'form-control underlined', 'type':'text','id':'user'}))

    password = forms.CharField(label="Contraseña",widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña',
        'class': 'form-control underlined', 'type':'password','id':'password'}))

class ProductoFormulario(forms.ModelForm):
    disponible = forms.IntegerField(
        min_value=0,
        label='Cantidad Disponible',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True
    )
    precio = forms.DecimalField(
        min_value=0,
        label='Precio',
        widget=forms.NumberInput(attrs={'placeholder': 'Precio del producto', 'id': 'precio', 'class': 'form-control'}),
        required=False
    )
    fecha_vencimiento = forms.DateField(
        initial=timezone.now,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Fecha de Vencimiento'
    )
    imagen_codigo = forms.ImageField(
        required=False,
        label='Imagen del Código',
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )
    imagen_producto = forms.ImageField(
        required=False,
        label='Imagen del Producto',
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )
    codigo_barra = forms.CharField(
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={'id': 'codigoBarra', 'class': 'form-control'})
    )
    
    class Meta:
        model = Producto
        fields = ['descripcion', 'precio', 'tipo', 'categoria', 'fecha_vencimiento', 'imagen_codigo', 'disponible', 'imagen_producto', 'codigo_barra']
        labels = {
            'descripcion': 'Nombre',
            'categoria': 'Categoría',
        }
        widgets = {
            'descripcion': forms.TextInput(attrs={'placeholder': 'Nombre del producto', 'id': 'descripcion', 'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control', 'id': 'tipo'}),
            'categoria': forms.Select(attrs={'class': 'form_control', 'id': 'categoria'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductoFormulario, self).__init__(*args, **kwargs)
        self.fields['tipo'].queryset = TipoProducto.objects.all()

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return precio

    def clean_disponible(self):
        disponible = self.cleaned_data.get('disponible')
        if disponible < 0:
            raise forms.ValidationError("La cantidad disponible no puede ser negativa.")
        return disponible


class ImportarProductosFormulario(forms.Form):
    importar = forms.FileField(
        max_length = 100000000000,
        label = 'Escoger archivo',
        widget = forms.ClearableFileInput(
        attrs={'id':'importar','class':'form-control'}),
        )

class ImportarClientesFormulario(forms.Form):
    importar = forms.FileField(
        max_length = 100000000000,
        label = 'Escoger archivo',
        widget = forms.ClearableFileInput(
        attrs={'id':'importar','class':'form-control'}),
        )   

class ExportarProductosFormulario(forms.Form):
    desde = forms.DateField(
        label = 'Desde',
        widget = forms.DateInput(format=('%d-%m-%Y'),
        attrs={'id':'desde','class':'form-control','type':'date'}),
        )   

    hasta = forms.DateField(
        label = 'Hasta',
        widget = forms.DateInput(format=('%d-%m-%Y'),
        attrs={'id':'hasta','class':'form-control','type':'date'}),
        )   

class ExportarClientesFormulario(forms.Form):
    desde = forms.DateField(
        label = 'Desde',
        widget = forms.DateInput(format=('%d-%m-%Y'),
        attrs={'id':'desde','class':'form-control','type':'date'}),
        )   

    hasta = forms.DateField(
        label = 'Hasta',
        widget = forms.DateInput(format=('%d-%m-%Y'),
        attrs={'id':'hasta','class':'form-control','type':'date'}),
        )   


class ClienteFormulario(forms.ModelForm):
    tipoC =  [ ('1','V'),('2','E') ]

    telefono2 = forms.CharField(
        required = False,
        label = 'Segundo numero telefonico',
        widget = forms.TextInput(
        attrs={'placeholder': 'Inserte el telefono alternativo del cliente',
        'id':'telefono2','class':'form-control'}),
        )

    correo2 = forms.CharField(
        required=False,
        label = 'Segundo correo electronico',
        widget = forms.TextInput(
        attrs={'placeholder': 'Inserte el correo alternativo del cliente',
        'id':'correo2','class':'form-control'}),
        )

    tipoCedula = forms.CharField(
        label="Tipo de cedula",
        max_length=2,
        widget=forms.Select(choices=tipoC,attrs={'placeholder': 'Tipo de cedula',
        'id':'tipoCedula','class':'form-control'}
        )
        )


class ClienteFormulario(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono', 'direccion', 'correo']  # Ajustar según los campos deseados
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'telefono': 'Teléfono',
            'direccion': 'Dirección (Opcional)',
            'correo': 'Correo electrónico (Opcional)',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
        }



class EmitirFacturaFormulario(forms.Form):
    def __init__(self, *args, **kwargs):
       elecciones = kwargs.pop('cedulas')
       super(EmitirFacturaFormulario, self).__init__(*args, **kwargs)

       if(elecciones):
            self.fields["cliente"] = forms.CharField(label="Cliente a facturar",max_length=50,
            widget=forms.Select(choices=elecciones,
            attrs={'placeholder': 'La cedula del cliente a facturar',
            'id':'cliente','class':'form-control'}))
    
    productos = forms.IntegerField(label="Numero de productos",widget=forms.NumberInput(attrs={'placeholder': 'Numero de productos a facturar',
        'id':'productos','class':'form-control'}))

class DetallesFacturaFormulario(forms.Form):
    productos = Producto.productosRegistrados()

    descripcion = MisProductos(queryset=productos,widget=forms.Select(attrs={'placeholder': 'El producto a debitar','class':'form-control select-group','onchange':'establecerOperaciones(this)'}))

    vista_precio = MisPrecios(required=False,queryset=productos,label="Precio del producto",widget=forms.Select(attrs={'placeholder': 'El precio del producto','class':'form-control','disabled':'true'}))

    cantidad = forms.IntegerField(label="Cantidad a facturar",min_value=0,widget=forms.NumberInput(attrs={'placeholder': 'Introduzca la cantidad del producto','class':'form-control','value':'0','onchange':'calculoPrecio(this);calculoDisponible(this)', 'max':'0'}))

    cantidad_disponibles = forms.IntegerField(required=False,label="Stock disponible",min_value=0,widget=forms.NumberInput(attrs={'placeholder': 'Introduzca la cantidad del producto','class':'form-control','value':'0', 'max':'0', 'disabled':'true'}))

    selec_disponibles = MisDisponibles(queryset=productos,required=False,widget=forms.Select(attrs={'placeholder': 'El producto a debitar','class':'form-control','disabled':'true','hidden':'true'}))

    subtotal = forms.DecimalField(required=False,label="Sub-total",min_value=0,widget=forms.NumberInput(attrs={'placeholder': 'Monto sub-total','class':'form-control','disabled':'true','value':'0'}))

    valor_subtotal = forms.DecimalField(min_value=0,widget=forms.NumberInput(attrs={'placeholder': 'Monto sub-total','class':'form-control','hidden':'true','value':'0'}))      


class EmitirPedidoFormulario(forms.Form):
    def __init__(self, *args, **kwargs):
       elecciones = kwargs.pop('cedulas')
       super(EmitirPedidoFormulario, self).__init__(*args, **kwargs)

       if(elecciones):
            self.fields["proveedor"] = forms.CharField(label="Proveedor",max_length=50,
            widget=forms.Select(choices=elecciones,attrs={'placeholder': 'La cedula del proveedor que vende el producto',
            'id':'proveedor','class':'form-control'}))

    productos = forms.IntegerField(label="Numero de productos",widget=forms.NumberInput(attrs={'placeholder': 'Numero de productos a comprar',
        'id':'productos','class':'form-control'}))


class DetallesPedidoFormulario(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DetallesPedidoFormulario, self).__init__(*args, **kwargs)

        # Mover la lógica de consulta a la base de datos al método __init__
        productos = Producto.productosRegistrados()
        precios = Producto.preciosProductos()

        # Inicializar los campos del formulario con los datos obtenidos
        self.fields['descripcion'] = MisProductos(queryset=productos, widget=forms.Select(attrs={'placeholder': 'El producto a debitar', 'class': 'form-control', 'onchange': 'establecerPrecio(this)'}))
        self.fields['vista_precio'] = MisPrecios(required=False, queryset=productos, label="Precio del producto", widget=forms.Select(attrs={'placeholder': 'El precio del producto', 'class': 'form-control', 'disabled': 'true'}))
        self.fields['cantidad'] = forms.IntegerField(label="Cantidad", min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Introduzca la cantidad del producto', 'class': 'form-control', 'value': '0', 'onchange': 'calculoPrecio(this)'}))
        self.fields['subtotal'] = forms.DecimalField(required=False, label="Sub-total", min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Monto sub-total', 'class': 'form-control', 'disabled': 'true', 'value': '0'}))
        self.fields['valor_subtotal'] = forms.DecimalField(min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Monto sub-total', 'class': 'form-control', 'hidden': 'true', 'value': '0'}))
      


class ProveedorFormulario(forms.ModelForm):
    tipoC =  [ ('1','V'),('2','E') ]

    telefono2 = forms.CharField(
        required = False,
        label = 'Segundo numero telefonico( Opcional )',
        widget = forms.TextInput(
        attrs={'placeholder': 'Inserte el telefono alternativo del proveedor',
        'id':'telefono2','class':'form-control'}),
        )

    correo2 = forms.CharField(
        required=False,
        label = 'Segundo correo electronico( Opcional )',
        widget = forms.TextInput(
        attrs={'placeholder': 'Inserte el correo alternativo del proveedor',
        'id':'correo2','class':'form-control'}),
        )

    tipoCedula = forms.CharField(
        label="Tipo de cedula",
        max_length=2,
        widget=forms.Select(choices=tipoC,attrs={'placeholder': 'Tipo de cedula',
        'id':'tipoCedula','class':'form-control'}
        )
        )


    class Meta:
        model = Cliente
        fields = ['tipoCedula','cedula','nombre','apellido','direccion','telefono','correo']
        labels = {
        'cedula': 'Cedula del proveedor',
        'nombre': 'Nombre del proveedor',
        'apellido': 'Apellido del proveedor',
        'direccion': 'Direccion del proveedor',
        'telefono': 'Numero telefonico del proveedor',
        'correo': 'Correo electronico del proveedor',
        'telefono2': 'Segundo numero telefonico',
        'correo2': 'Segundo correo electronico'
        }
        widgets = {
        'cedula': forms.TextInput(attrs={'placeholder': 'Inserte la cedula de identidad del proveedor',
        'id':'cedula','class':'form-control'} ),
        'nombre': forms.TextInput(attrs={'placeholder': 'Inserte el primer o primeros nombres del proveedor',
        'id':'nombre','class':'form-control'}),
        'apellido': forms.TextInput(attrs={'class':'form-control','id':'apellido','placeholder':'El apellido del proveedor'}),
        'direccion': forms.TextInput(attrs={'class':'form-control','id':'direccion','placeholder':'Direccion del proveedor'}), 
        'telefono':forms.TextInput(attrs={'id':'telefono','class':'form-control',
        'placeholder':'El telefono del proveedor'} ),
        'correo':forms.TextInput(attrs={'placeholder': 'Correo del proveedor',
        'id':'correo','class':'form-control'} )
        } 


class UsuarioFormulario(forms.Form):
    niveles =  [ ('1','Administrador'),('0','Usuario') ]

    username = forms.CharField(
        label = "Nombre de usuario",
        max_length=50,
        widget = forms.TextInput(attrs={'placeholder': 'Inserte un nombre de usuario',
        'id':'username','class':'form-control','value':''} ),
        )

    first_name = forms.CharField(
        label = 'Nombre',
        max_length =100,
        widget = forms.TextInput(attrs={'placeholder': 'Inserte un nombre',
        'id':'first_name','class':'form-control','value':''}),            
        )

    last_name = forms.CharField(
        label = 'Apellido',
        max_length = 100,
        widget = forms.TextInput(attrs={'class':'form-control','id':'last_name','placeholder':'Inserte un apellido','value':''}), 
        )

    email = forms.CharField(
        label = 'Correo electronico',
        max_length=100,
        widget = forms.TextInput(attrs={'placeholder': 'Inserte un correo valido',
        'id':'email','class':'form-control','type':'email','value':''} )
        )

    level =  forms.CharField(
        required=False,
        label="Nivel de acceso",
        max_length=2,
        widget=forms.Select(choices=niveles,attrs={'placeholder': 'El nivel de acceso',
        'id':'level','class':'form-control','value':''}
        )
        )

class NuevoUsuarioFormulario(forms.Form):
    niveles =  [ ('1','Administrador'),('0','Usuario') ]

    username = forms.CharField(
        label = "Nombre de usuario",
        max_length=50,
        widget = forms.TextInput(attrs={'placeholder': 'Inserte un nombre de usuario',
        'id':'username','class':'form-control','value':''} ),
        )

    first_name = forms.CharField(
        label = 'Nombre',
        max_length =100,
        widget = forms.TextInput(attrs={'placeholder': 'Inserte un nombre',
        'id':'first_name','class':'form-control','value':''}),            
        )

    last_name = forms.CharField(
        label = 'Apellido',
        max_length = 100,
        widget = forms.TextInput(attrs={'class':'form-control','id':'last_name','placeholder':'Inserte un apellido','value':''}), 
        )

    email = forms.CharField(
        label = 'Correo electronico',
        max_length=100,
        widget = forms.TextInput(attrs={'placeholder': 'Inserte un correo valido',
        'id':'email','class':'form-control','type':'email','value':''} )
        )    

    password = forms.CharField(
        label = 'Clave',
        max_length=100,
        widget = forms.TextInput(attrs={'placeholder': 'Inserte una clave',
        'id':'password','class':'form-control','type':'password','value':''} )
        )  

    rep_password = forms.CharField(
        label = 'Repetir clave',
        max_length=100,
        widget = forms.TextInput(attrs={'placeholder': 'Repita la clave de arriba',
        'id':'rep_password','class':'form-control','type':'password','value':''} )
        )  

    level =  forms.CharField(
        label="Nivel de acceso",
        max_length=2,
        widget=forms.Select(choices=niveles,attrs={'placeholder': 'El nivel de acceso',
        'id':'level','class':'form-control','value':''}
        )
        )


class ClaveFormulario(forms.Form):
    #clave = forms.CharField(
        #label = 'Ingrese su clave actual',
        #max_length=50,
        #widget = forms.TextInput(
        #attrs={'placeholder': 'Inserte la clave actual para verificar su identidad',
        #'id':'clave','class':'form-control', 'type': 'password'}),
        #)

    clave_nueva = forms.CharField(
        label = 'Ingrese la clave nueva',
        max_length=50,
        widget = forms.TextInput(
        attrs={'placeholder': 'Inserte la clave nueva de acceso',
        'id':'clave_nueva','class':'form-control', 'type': 'password'}),
        )

    repetir_clave = forms.CharField(
        label="Repita la clave nueva",
        max_length=50,
        widget = forms.TextInput(
        attrs={'placeholder': 'Vuelva a insertar la clave nueva',
        'id':'repetir_clave','class':'form-control', 'type': 'password'}),
        )


class ImportarBDDFormulario(forms.Form):
    archivo = forms.FileField(
        widget=forms.FileInput(
            attrs={'placeholder': 'Archivo de la base de datos',
            'id':'customFile','class':'custom-file-input'})
        )

class OpcionesFormulario(forms.Form):
    moneda = forms.CharField(
        label = 'Moneda a emplear en el sistema',
        max_length=20,
        widget = forms.TextInput(
        attrs={'placeholder': 'Inserte la abreviatura de la moneda que quiere usar (Ejemplo: $)',
        'id':'moneda','class':'form-control'}),
        )


    mensaje_factura = forms.CharField(
        label = 'Mensaje personal que va en las facturas',
        max_length=50,
        widget = forms.TextInput(
        attrs={'placeholder': 'Inserte el mensaje personal que ira en el pie de la factura',
        'id':'mensaje_factura','class':'form-control'}),
        )

    nombre_negocio = forms.CharField(
        label = 'Nombre actual del negocio',
        max_length=50,
        widget = forms.TextInput(
        attrs={'class':'form-control','id':'nombre_negocio',
            'placeholder':'Coloque el nombre actual del negocio'}),
        )

    imagen = forms.FileField(required=False,widget = forms.FileInput(
        attrs={'class':'custom-file-input','id':'customFile'}))


    valor_iva = forms.DecimalField(
        label='Valor del IVA',
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el valor del IVA, ej. 16.00'
        })
    )

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']


class ImpuestoForm(forms.ModelForm):
    class Meta:
        model = Impuesto
        fields = ['nombre', 'tasa']


## V E N T A S ---------------------------------------------------

from django import forms

class FiltroVentasForm(forms.Form):
    fecha_inicio = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))


## FINAL FORMULARIO-----------------------------------------------