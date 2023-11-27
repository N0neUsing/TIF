from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "inventario"

urlpatterns = [
path('login', views.Login.as_view(), name='login'),
path('panel', views.Panel.as_view(), name='panel'),
path('salir', views.Salir.as_view(), name='salir'),
path('perfil/<str:modo>/<int:p>', views.Perfil.as_view(), name='perfil'),
path('eliminar/<str:modo>/<int:p>', views.Eliminar.as_view(), name='eliminar'),

path('listarProductos', views.ListarProductos.as_view(), name='listarProductos'),
path('agregarProducto', views.AgregarProducto.as_view(), name='agregarProducto'),
path('importarProductos', views.ImportarProductos.as_view(), name='importarProductos'),
path('exportarProductos', views.ExportarProductos.as_view(), name='exportarProductos'),
path('escanear', views.EscanearProducto.as_view(), name='escanear_codigo'),
path('editarProducto/<int:id>/', views.EditarProducto.as_view(), name='editar_producto'),
path('preciosProducto', views.PreciosProducto.as_view(), name='preciosProducto'),

path('listarProveedores', views.ListarProveedores.as_view(), name='listarProveedores'),
path('agregarProveedor', views.AgregarProveedor.as_view(), name='agregarProveedor'),
path('importarProveedores', views.ImportarProveedores.as_view(), name='importarProveedores'),
path('exportarProveedores', views.ExportarProveedores.as_view(), name='exportarProveedores'),
path('editarProveedor/<int:p>', views.EditarProveedor.as_view(), name='editarProveedor'),

path('agregarPedido', views.AgregarPedido.as_view(), name='agregarPedido'),
path('listarPedidos', views.ListarPedidos.as_view(), name='listarPedidos'),
path('detallesPedido', views.DetallesPedido.as_view(), name='detallesPedido'),
path('verPedido/<int:p>',views.VerPedido.as_view(), name='verPedido'),
path('validarPedido/<int:p>',views.ValidarPedido.as_view(), name='validarPedido'),
path('generarPedido/<int:p>',views.GenerarPedido.as_view(), name='generarPedido'),
path('generarPedidoPDF/<int:p>',views.GenerarPedidoPDF.as_view(), name='generarPedidoPDF'),

path('listarClientes', views.ListarClientes.as_view(), name='listarClientes'),
path('agregarCliente', views.AgregarCliente.as_view(), name='agregarCliente'),
path('importarClientes', views.ImportarClientes.as_view(), name='importarClientes'),
path('exportarClientes', views.ExportarClientes.as_view(), name='exportarClientes'),
path('editarCliente/<int:p>', views.EditarCliente.as_view(), name='editarCliente'),

path('emitirFactura', views.EmitirFactura.as_view(), name='emitirFactura'),
path('detallesDeFactura', views.DetallesFactura.as_view(), name='detallesDeFactura'),
path('listarFacturas',views.ListarFacturas.as_view(), name='listarFacturas'),
path('verFactura/<int:p>',views.VerFactura.as_view(), name='verFactura'),
path('generarFactura/<int:p>',views.GenerarFactura.as_view(), name='generarFactura'),
path('generarFacturaPDF/<int:p>',views.GenerarFacturaPDF.as_view(), name='generarFacturaPDF'),

path('crearUsuario',views.CrearUsuario.as_view(), name='crearUsuario'),
path('listarUsuarios', views.ListarUsuarios.as_view(), name='listarUsuarios'),

path('importarBDD',views.ImportarBDD.as_view(), name='importarBDD'),
path('descargarBDD', views.DescargarBDD.as_view(), name='descargarBDD'),
path('configuracionGeneral', views.ConfiguracionGeneral.as_view(), name='configuracionGeneral'),

path('verManualDeUsuario/<str:pagina>/',views.VerManualDeUsuario.as_view(), name='verManualDeUsuario'),

path('categorias/', views.lista_categorias, name='lista_categorias'),
path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
path('categorias/editar/<int:id>/', views.editar_categoria, name='editar_categoria'),
path('categorias/eliminar/<int:id>/', views.eliminar_categoria, name='eliminar_categoria'),

path('carrito/', views.CartView.as_view(), name='cart'),
path('agregar-a-carrito/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
path('actualizar-item-carrito/<int:product_id>/', views.UpdateCartItemView.as_view(), name='update_cart_item'),
path('eliminar-de-carrito/<int:product_id>/', views.RemoveFromCart.as_view(), name='remove_from_cart'),
path('checkout/', views.Checkout.as_view(), name='checkout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

