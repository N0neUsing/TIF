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
path('filtrar-ingresos/', views.FiltrarIngresosView.as_view(), name='filtrar_ingresos'),


path('listarProductos', views.ListarProductos.as_view(), name='listarProductos'),
path('agregarProducto', views.AgregarProducto.as_view(), name='agregarProducto'),
path('importarProductos', views.ImportarProductos.as_view(), name='importarProductos'),
path('exportarProductos', views.ExportarProductos.as_view(), name='exportarProductos'),
path('escanear', views.EscanearProducto.as_view(), name='escanear_codigo'),
path('editarProducto/<int:id>/', views.EditarProducto.as_view(), name='editar_producto'),
path('editarProducto/<str:codigo_barra>/', views.EditarProducto.as_view(), name='editar_producto'),
path('preciosProducto', views.PreciosProducto.as_view(), name='preciosProducto'),
path('api/producto/<str:codigo_barra>/', views.ObtenerProductoPorCodigo.as_view(), name='obtener_producto_por_codigo'),
path('api/precioProducto/<int:id>/', views.PrecioProductoAPI.as_view(), name='precioProductoAPI'),
path('actualizar-precio/<int:product_id>/', views.UpdateProductPriceView.as_view(), name='actualizar-precio'),
path('pagar-cuenta-cliente/', views.PagarCuentaClienteView.as_view(), name='pagar-cuenta-cliente'),
path('api/buscar-productos/', views.buscar_productos, name='buscar_productos'),



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
path('api/clientes/', views.ApiClientes.as_view(), name='api_clientes'),
path('api/cliente/<int:client_id>/productos/', views.ClientProductsView.as_view(), name='client-products'),
path('asignar-carrito-a-cliente/', views.AssignCartToClientView.as_view(), name='assign-cart-to-client'),
path('pagar-cuenta-cliente/<int:cliente_id>/', views.PagarCuentaClienteView.as_view(), name='pagar-cuenta-cliente'),
path('eliminarCliente/<int:pk>/', views.EliminarClienteView.as_view(), name='eliminarCliente'),
path('editarCliente/<int:pk>/', views.EditarClienteView.as_view(), name='editarCliente'),
path('api/cliente/<int:pk>/', views.ObtenerClienteView.as_view(), name='obtener_cliente'),




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
path('eliminar-de-carrito/<int:product_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
path('checkout/', views.Checkout.as_view(), name='checkout'),
path('agregar-producto-por-codigo/', views.AgregarProductoPorCodigo.as_view(), name='agregar_producto_por_codigo'),
path('api/cart/', views.CartListCreateAPIView.as_view(), name='api_cart_list_create'),
path('api/cart/items/', views.CartItemCreateAPIView.as_view(), name='api_cartitem_create'),

path('impuestos/', views.ListarImpuestos.as_view(), name='listarImpuestos'),
path('impuestos/crear/', views.CrearImpuesto.as_view(), name='crearImpuesto'),
path('impuestos/editar/<int:id>/', views.EditarImpuesto.as_view(), name='editarImpuesto'),
path('impuestos/eliminar/<int:id>/', views.EliminarImpuesto.as_view(), name='eliminarImpuesto'),
path('api/total-con-impuestos/', views.TotalConImpuestosView.as_view(), name='total_con_impuestos'),


path('ventas/listar_ventas/', views.VentasView.as_view(), name='listar_ventas'),
path('ventas/eliminar/', views.EliminarVentaView.as_view(), name='eliminar_venta'),
path('ventas/imprimir_ticket/<int:venta_id>/', views.ImprimirTicketView.as_view(), name='imprimir_ticket'),
path('ventas-avanzadas/', views.ventas_avanzadas, name='ventas_avanzadas'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

