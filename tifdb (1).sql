-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-11-2023 a las 18:08:29
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `tifdb`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL DEFAULT 0,
  `permission_id` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `content_type_id` int(11) NOT NULL DEFAULT 0,
  `codename` varchar(100) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `content_type_id`, `codename`, `name`) VALUES
(1, 1, 'add_usuario', 'Can add user'),
(2, 1, 'change_usuario', 'Can change user'),
(3, 1, 'delete_usuario', 'Can delete user'),
(4, 1, 'view_usuario', 'Can view user'),
(5, 2, 'add_logentry', 'Can add log entry'),
(6, 2, 'change_logentry', 'Can change log entry'),
(7, 2, 'delete_logentry', 'Can delete log entry'),
(8, 2, 'view_logentry', 'Can view log entry'),
(9, 3, 'add_permission', 'Can add permission'),
(10, 3, 'change_permission', 'Can change permission'),
(11, 3, 'delete_permission', 'Can delete permission'),
(12, 3, 'view_permission', 'Can view permission'),
(13, 4, 'add_group', 'Can add group'),
(14, 4, 'change_group', 'Can change group'),
(15, 4, 'delete_group', 'Can delete group'),
(16, 4, 'view_group', 'Can view group'),
(17, 5, 'add_contenttype', 'Can add content type'),
(18, 5, 'change_contenttype', 'Can change content type'),
(19, 5, 'delete_contenttype', 'Can delete content type'),
(20, 5, 'view_contenttype', 'Can view content type'),
(21, 6, 'add_session', 'Can add session'),
(22, 6, 'change_session', 'Can change session'),
(23, 6, 'delete_session', 'Can delete session'),
(24, 6, 'view_session', 'Can view session'),
(25, 7, 'add_producto', 'Can add producto'),
(26, 7, 'change_producto', 'Can change producto'),
(27, 7, 'delete_producto', 'Can delete producto'),
(28, 7, 'view_producto', 'Can view producto'),
(29, 8, 'add_detallefactura', 'Can add detalle factura'),
(30, 8, 'change_detallefactura', 'Can change detalle factura'),
(31, 8, 'delete_detallefactura', 'Can delete detalle factura'),
(32, 8, 'view_detallefactura', 'Can view detalle factura'),
(33, 9, 'add_factura', 'Can add factura'),
(34, 9, 'change_factura', 'Can change factura'),
(35, 9, 'delete_factura', 'Can delete factura'),
(36, 9, 'view_factura', 'Can view factura'),
(37, 10, 'add_cliente', 'Can add cliente'),
(38, 10, 'change_cliente', 'Can change cliente'),
(39, 10, 'delete_cliente', 'Can delete cliente'),
(40, 10, 'view_cliente', 'Can view cliente'),
(41, 11, 'add_configuracionfactura', 'Can add configuracion factura'),
(42, 11, 'change_configuracionfactura', 'Can change configuracion factura'),
(43, 11, 'delete_configuracionfactura', 'Can delete configuracion factura'),
(44, 11, 'view_configuracionfactura', 'Can view configuracion factura'),
(45, 12, 'add_detallepedido', 'Can add detalle pedido'),
(46, 12, 'change_detallepedido', 'Can change detalle pedido'),
(47, 12, 'delete_detallepedido', 'Can delete detalle pedido'),
(48, 12, 'view_detallepedido', 'Can view detalle pedido'),
(49, 13, 'add_opciones', 'Can add opciones'),
(50, 13, 'change_opciones', 'Can change opciones'),
(51, 13, 'delete_opciones', 'Can delete opciones'),
(52, 13, 'view_opciones', '41-TRIAL-Can view opciones 167'),
(53, 14, 'add_pedido', '34-TRIAL-Can add pedido 100'),
(54, 14, 'change_pedido', '269-TRIAL-Can change pedido 124'),
(55, 14, 'delete_pedido', '78-TRIAL-Can delete pedido 258'),
(56, 14, 'view_pedido', '262-TRIAL-Can view pedido 164'),
(57, 15, 'add_proveedor', '5-TRIAL-Can add proveedor 245'),
(58, 15, 'change_proveedor', '181-TRIAL-Can change proveedor 27'),
(59, 15, 'delete_proveedor', '61-TRIAL-Can delete proveedor 191'),
(60, 15, 'view_proveedor', '295-TRIAL-Can view proveedor 242'),
(61, 16, 'add_notificaciones', '27-TRIAL-Can add notificaciones 36'),
(62, 16, 'change_notificaciones', '291-TRIAL-Can change notificaciones 204'),
(63, 16, 'delete_notificaciones', '2-TRIAL-Can delete notificaciones 153'),
(64, 16, 'view_notificaciones', '292-TRIAL-Can view notificaciones 82'),
(65, 17, 'add_categoria', 'Can add categoria'),
(66, 17, 'change_categoria', 'Can change categoria'),
(67, 17, 'delete_categoria', 'Can delete categoria'),
(68, 17, 'view_categoria', 'Can view categoria'),
(69, 18, 'add_precioscraping', 'Can add precio scraping'),
(70, 18, 'change_precioscraping', 'Can change precio scraping'),
(71, 18, 'delete_precioscraping', 'Can delete precio scraping'),
(72, 18, 'view_precioscraping', 'Can view precio scraping'),
(73, 19, 'add_cartitem', 'Can add cart item'),
(74, 19, 'change_cartitem', 'Can change cart item'),
(75, 19, 'delete_cartitem', 'Can delete cart item'),
(76, 19, 'view_cartitem', 'Can view cart item'),
(77, 20, 'add_cart', 'Can add cart'),
(78, 20, 'change_cart', 'Can change cart'),
(79, 20, 'delete_cart', 'Can delete cart'),
(80, 20, 'view_cart', 'Can view cart');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime NOT NULL,
  `object_id` text DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `change_message` text NOT NULL,
  `content_type_id` int(11) DEFAULT 0,
  `user_id` bigint(20) NOT NULL,
  `action_flag` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(2, 'admin', 'logentry'),
(4, 'auth', 'group'),
(3, 'auth', 'permission'),
(5, 'contenttypes', 'contenttype'),
(20, 'inventario', 'cart'),
(19, 'inventario', 'cartitem'),
(17, 'inventario', 'categoria'),
(10, 'inventario', 'cliente'),
(11, 'inventario', 'configuracionfactura'),
(8, 'inventario', 'detallefactura'),
(12, 'inventario', 'detallepedido'),
(9, 'inventario', 'factura'),
(16, 'inventario', 'notificaciones'),
(13, 'inventario', 'opciones'),
(14, 'inventario', 'pedido'),
(18, 'inventario', 'precioscraping'),
(7, 'inventario', 'producto'),
(15, 'inventario', 'proveedor'),
(1, 'inventario', 'usuario'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2019-03-14 15:28:21'),
(2, 'contenttypes', '0002_remove_content_type_name', '2019-03-14 15:28:21'),
(3, 'auth', '0001_initial', '2019-03-14 15:28:21'),
(4, 'auth', '0002_alter_permission_name_max_length', '2019-03-14 15:28:22'),
(5, 'auth', '0003_alter_user_email_max_length', '2019-03-14 15:28:22'),
(6, 'auth', '0004_alter_user_username_opts', '2019-03-14 15:28:22'),
(7, 'auth', '0005_alter_user_last_login_null', '2019-03-14 15:28:22'),
(8, 'auth', '0006_require_contenttypes_0002', '2019-03-14 15:28:22'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2019-03-14 15:28:22'),
(10, 'auth', '0008_alter_user_username_max_length', '2019-03-14 15:28:22'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2019-03-14 15:28:22'),
(12, 'inventario', '0001_initial', '2019-03-14 15:28:23'),
(13, 'admin', '0001_initial', '2019-03-14 15:28:23'),
(14, 'admin', '0002_logentry_remove_auto_add', '2019-03-14 15:28:23'),
(15, 'admin', '0003_logentry_add_action_flag_choices', '2019-03-14 15:28:23'),
(16, 'sessions', '0001_initial', '2019-03-14 15:28:23'),
(17, 'inventario', '0002_auto_20190317_0107', '2019-03-17 01:07:34'),
(18, 'inventario', '0003_auto_20190317_1656', '2019-03-17 16:56:23'),
(19, 'inventario', '0004_notificaciones', '2019-04-08 23:18:20'),
(20, 'inventario', '0005_auto_20190418_0109', '2019-04-18 01:09:54'),
(21, 'inventario', '0006_auto_20190428_2056', '2019-04-28 20:56:43'),
(22, 'inventario', '0007_auto_20160211_1800', '2016-02-11 18:00:39'),
(23, 'inventario', '0008_auto_20190826_0447', '2019-08-26 04:47:46'),
(24, 'inventario', '0009_usuario_nivel', '2016-02-11 18:00:36'),
(25, 'inventario', '0010_opciones_logo', '2019-11-23 13:13:39'),
(26, 'inventario', '0011_remove_opciones_logo', '2019-11-23 19:41:44'),
(27, 'inventario', '0012_auto_20191126_0126', '2019-11-26 01:27:08'),
(28, 'inventario', '0013_auto_20191126_0129', '2019-11-26 01:30:00'),
(29, 'inventario', '0014_auto_20200609_1526', '2020-06-09 15:26:16'),
(30, 'auth', '0010_alter_group_name_max_length', '2023-10-29 11:46:48'),
(31, 'auth', '0011_update_proxy_permissions', '2023-10-29 11:46:48'),
(32, 'auth', '0012_alter_user_first_name_max_length', '2023-10-29 11:46:48'),
(33, 'inventario', '0015_categoria_producto_codigo_barra_and_more', '2023-11-19 21:40:42'),
(34, 'inventario', '0016_producto_categoria_producto_imagen_codigo_and_more', '2023-11-20 22:12:53'),
(35, 'inventario', '0017_precioscraping', '2023-11-21 16:20:04'),
(36, 'inventario', '0018_cart_cartitem', '2023-11-22 12:50:13');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` text NOT NULL,
  `expire_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('02paiqd1k0ii6ikqolvqxlcru9zqjkgd', 'ZTk2MzU0NDIwYmFiZjA3OTc3OGFlMDg0ZTUxMjE0YjNhZTk3YjI3Zjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxY2IzZDNhYmRlYWZmMWMzNTEzNzQzYWJmNTg5NDEwNTNmZjBjZmNiIn0=', '2016-02-25 21:01:25'),
('03gnn4wou8nq6a0a4zzx5kpv6mjnklz2', 'ZTk2MzU0NDIwYmFiZjA3OTc3OGFlMDg0ZTUxMjE0YjNhZTk3YjI3Zjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxY2IzZDNhYmRlYWZmMWMzNTEzNzQzYWJmNTg5NDEwNTNmZjBjZmNiIn0=', '2019-09-10 18:42:02'),
('0azd2l1s07nth6h8wqtwxecwallvre43', 'YTU1OGVhMjM0Njg4NTM4ZmQxZGExZDM4ZDI0NTM5ZTg5ZGI2ODYyYTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiMWNiM2QzYWJkZWFmZjFjMzUxMzc0M2FiZjU4OTQxMDUzZmYwY2ZjYiIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2019-10-07 18:22:54'),
('0dxhbtm6tghxychr07lcptzozadtt1kv', 'NTgyMTc2ZjAyYTI0OGYyMWE3ODRiZGYzYTRhNWM0M2QxMjQwZGI2Zjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiOGYxMzcwOGJiMDYyM2YzYTk0MTE1NjQxMWQzNWMxZjBkZjI2ZGQ4MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-09-02 21:17:20'),
('0jwda9yzjmxcyas7epr9y2ljg993vplh', 'MzljYWQxNmJkOWMzYTJhNzg4NDM3NjgwOTI4OTdkNGQ3ZmE3ZDI1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwiZm9ybV9kZXRhaWxzIjoyLCJpZF9jbGllbnQiOiI1NyJ9', '2019-04-24 23:34:10'),
('0kc9a0k0bv0y7vyl6b18p2clvva7dc0h', 'YTgzZTJkYWU2MWY0ODU1OTQ3OGY5OGYwYzRiNGMxZTdkMzBjZDNmYzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJwZXJmaWxQcm9jZXNhZG8iOnRydWUsIl9hdXRoX3VzZXJfaGFzaCI6IjFjYjNkM2FiZGVhZmYxYzM1MTM3NDNhYmY1ODk0MTA1M2ZmMGNmY2IifQ==', '2016-02-25 18:47:58'),
('0tmnrgpe0nq3meexnhedogiy3erzth8z', 'YzI2NjM1ODU2M2QyMjljYmRiMzIxNjljM2UxODU0NmFlNzg0MWI4Mjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiaWRfY2xpZW50IjoiMjYxNzgxNTQiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfaGFzaCI6IjhmMTM3MDhiYjA2MjNmM2E5NDExNTY0MTFkMzVjMWYwZGYyNmRkODAiLCJmb3JtX2RldGFpbHMiOjF9', '2016-02-25 20:05:03'),
('0umpyqj2ftise60ldv2lrf0mpphmd1mt', 'NGIxNmZkYjEyMmM4ODljMGQ0ZDcyNmEyM2JlODFkNGM5NzkxNjgxZTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiMWNiM2QzYWJkZWFmZjFjMzUxMzc0M2FiZjU4OTQxMDUzZmYwY2ZjYiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-10-09 01:20:52'),
('0uu5krksfy27hedmt33l272pyxtxgven', 'Y2FmZjFkODc3Y2M5YTFiYTBlMDlkMGMxODllY2I5MzU1NTcwMGFjMzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwiaWRfY2xpZW50IjoiMjYxNzgxNjQ4OSIsImZvcm1fZGV0YWlscyI6MX0=', '2016-02-25 16:38:54'),
('0x6lccu6tu073r127cxz5n49y58ob1fq', 'ZGExNDRiNjU1MzcyMzk5ZDM4NjE3MDc2ZjU3M2RiYWVjMjI3OTMzYTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwicHJvdmVlZG9yUHJvY2VzYWRvIjoiZWRpdGFkbyIsImZvcm1fZGV0YWlscyI6MSwiaWRfcHJvdmVlZG9yIjoiMjc4NDQ1MzEiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQifQ==', '2016-02-25 17:11:32'),
('19xu1ds0o3v60b7i0kh20ch9r1aygvwt', 'YzcwNjM1ODc2Y2Q1MTJkNTc1OGExYzQ1OTExNWFkNmM4Mzk5N2VjNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiaWRfY2xpZW50IjoiMjYxNzgxNTQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjhmMTM3MDhiYjA2MjNmM2E5NDExNTY0MTFkMzVjMWYwZGYyNmRkODAiLCJmb3JtX2RldGFpbHMiOjJ9', '2016-02-25 21:29:54'),
('1byk8lmxyx38o40gnzet7n6f5h541ex4', 'MDI4ZjQ2ZGY3ZTI5ZDUxNTk5ZTliZTg5MjIxMTgyMTZjZTUwMTg0Yjp7ImlkX2NsaWVudCI6IjI2MTc4MTU0IiwiX2F1dGhfdXNlcl9oYXNoIjoiOGYxMzcwOGJiMDYyM2YzYTk0MTE1NjQxMWQzNWMxZjBkZjI2ZGQ4MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiZm9ybV9kZXRhaWxzIjoyLCJfYXV0aF91c2VyX2lkIjoiMSJ9', '2016-02-25 17:00:17'),
('1klv9bvpkcw9kw6d387otdnmzdgym5rs', 'YWMzMGJmMWZkMDYzMGU3NGYyNDg1OWU5Zjc2ZTcwNzEwMjc3MWM3ODp7ImlkX2NsaWVudCI6IjI2MTc4MTU0IiwiX2F1dGhfdXNlcl9oYXNoIjoiOGYxMzcwOGJiMDYyM2YzYTk0MTE1NjQxMWQzNWMxZjBkZjI2ZGQ4MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJmb3JtX2RldGFpbHMiOjF9', '2016-02-25 20:56:31'),
('1qh9h61jyithymf59c4lp44pe8g84yua', 'NDdhY2ZiODAzMWFkMzY3MWRlYzdkM2Y2Y2NmM2FmNWM5MjY5NDRmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2019-04-15 16:22:03'),
('1qo3rxzq6u43fv0u2idbrfp15g41j1lc', 'ZTk2MzU0NDIwYmFiZjA3OTc3OGFlMDg0ZTUxMjE0YjNhZTk3YjI3Zjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxY2IzZDNhYmRlYWZmMWMzNTEzNzQzYWJmNTg5NDEwNTNmZjBjZmNiIn0=', '2016-02-25 19:12:47'),
('1vgzi1mx6oqt8qi3xyo5pi23sbx58ydj', 'MGQ0YmI4YjE5NDZjZDE0MGRmYzQ1NjcxMDAxN2VmMGU5NGU3ZDRkYTp7Il9hdXRoX3VzZXJfaGFzaCI6IjFjYjNkM2FiZGVhZmYxYzM1MTM3NDNhYmY1ODk0MTA1M2ZmMGNmY2IiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2016-02-25 17:52:47'),
('294n58t2n9zr3vjpsyj77yr0u2nwy8px', 'NDdhY2ZiODAzMWFkMzY3MWRlYzdkM2Y2Y2NmM2FmNWM5MjY5NDRmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2019-04-17 21:24:10'),
('2k4na1gnk1r8bkslizhx93qilx9ny0iz', 'NGIxNmZkYjEyMmM4ODljMGQ0ZDcyNmEyM2JlODFkNGM5NzkxNjgxZTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiMWNiM2QzYWJkZWFmZjFjMzUxMzc0M2FiZjU4OTQxMDUzZmYwY2ZjYiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-12-06 21:37:54'),
('2uvy44o59bb0tngs6il4udqbls4ewudd', 'MWQyNjRmODY5NWVhNDQzMjhjYzM1MDhiNjFhZDIwNWZhZmFlMTQ0Yzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOGYxMzcwOGJiMDYyM2YzYTk0MTE1NjQxMWQzNWMxZjBkZjI2ZGQ4MCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2016-02-25 17:05:19'),
('34xcowe97d26ovyzqf6tfpjbleff82zv', 'NjUzYWQ4ZmFiZTUzNzAxMTRhYmQ3ZWE0Mjk1MmJjYTg1NTMyODdkNzp7ImZvcm1fZGV0YWlscyI6MSwiX2F1dGhfdXNlcl9pZCI6IjEiLCJpZF9jbGllbnQiOiIyNjE3ODE1NCIsIl9hdXRoX3VzZXJfaGFzaCI6IjhmMTM3MDhiYjA2MjNmM2E5NDExNTY0MTFkMzVjMWYwZGYyNmRkODAiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9', '2016-02-26 03:00:49'),
('40gk3583dhbtvj6qdgkn5ocmx4n4lsto', 'ZGIwOGRjYmYyYWFmYjUyYmYyYzNiY2E4ODBmZWU1MDdkN2E1MzY0ZDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwiZm9ybV9kZXRhaWxzIjoyLCJpZF9jbGllbnQiOiIyNjE3ODE2NSJ9', '2019-04-22 23:15:16'),
('43rojqh3an09re83sj6azvfggtq7w7us', 'YjAzN2RmZDU0MjIzYjRmMzEyYjFiZWE0MjZmZTg1Mjc3MTllOGNiZTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhmMTM3MDhiYjA2MjNmM2E5NDExNTY0MTFkMzVjMWYwZGYyNmRkODAiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2016-02-25 17:00:52'),
('4dx2mnczqzi0gza10soai1mmagu9nj8n', 'NDdhY2ZiODAzMWFkMzY3MWRlYzdkM2Y2Y2NmM2FmNWM5MjY5NDRmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2019-03-28 15:47:07'),
('4lgo70z33yi332h0jm334t11iganeyud', 'ZjU5MmMxYWJkMGNkZTAxZmRmMTM4ZTM2ZmI4MTAwOGZmNTJiMzYzZDp7ImlkX3Byb3ZlZWRvciI6Ijg1NDE5NDMyIiwiaWRfY2xpZW50IjoiOTk1Njc4MjEiLCJfYXV0aF91c2VyX2lkIjoiMSIsImZvcm1fZGV0YWlscyI6MSwiX2F1dGhfdXNlcl9oYXNoIjoiMWNiM2QzYWJkZWFmZjFjMzUxMzc0M2FiZjU4OTQxMDUzZmYwY2ZjYiIsInBlcmZpbFByb2Nlc2FkbyI6dHJ1ZSwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJjbGllbnRlUHJvY2VzYWRvIjoiYWdyZWdhZG8iLCJwcm92ZWVkb3JQcm9jZXNhZG8iOiJhZ3JlZ2FkbyJ9', '2019-10-05 22:24:24'),
('4ngwbhf81zvba9o489tfpcb7qoo9597m', 'MGQ0YmI4YjE5NDZjZDE0MGRmYzQ1NjcxMDAxN2VmMGU5NGU3ZDRkYTp7Il9hdXRoX3VzZXJfaGFzaCI6IjFjYjNkM2FiZGVhZmYxYzM1MTM3NDNhYmY1ODk0MTA1M2ZmMGNmY2IiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2019-12-05 01:59:31'),
('4zzp3xdfovvhviww002s3gcyz8cpld52', '.eJxVjE0OgjAQhe_StWmgYGldujfxBmQ6MwXUMKSFlfHuloSFbiZv3s_3Vj1s69hvmVM_kboop06_XgB88rwH9IB5EI0yr2kKeq_oI836JsSv69H9A4yQx7L2lbdM6Oqzgyq4znfOkGkbF6MH6yK2QMGaWEUAi11dbs2-_NgQG4ACXZLQhqvckyBnIClYGBIPu_x8AXeQQ9g:1qx5Xr:bcCJqE2vjVyx0q7FZOgRYCa7LjCJLIS5531WShZW0fA', '2023-11-12 13:09:35'),
('5at4ovud4x6dzqtlhdhs11559d27ebu7', '.eJxVjMEOwiAQRP-FsyFAKywevfsNZNkFqRpISnsy_rtt0oNeJpl5M_MWAdelhLWnOUwsLgLE6TeLSM9Ud8APrPcmqdVlnqLcK_KgXd4ap9f16P4dFOxlW3vlbWICfQZUEZx3YNiMA-Ts0UKmETlak1VGtOT0pjr5zdPAySCKzxfqDzig:1r3dC3:DeVDnsftVJVCUqdbScJcZUyMCiJHyRpFZoa3POeyIGI', '2023-11-30 14:18:07'),
('5rp8pydr2mkr861t7kuahufuhrgk4y7u', 'OWMwNzlhZTUyZjFiNDg1MGUxZjk0ZWE0NzE3N2JjMzg4MzBhNjA5MTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiZm9ybV9kZXRhaWxzIjoyLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJpZF9jbGllbnQiOiIyNSJ9', '2019-05-24 00:32:24'),
('60alsopi6mgvopsprep3tp5ermaeq7t0', 'NDdhY2ZiODAzMWFkMzY3MWRlYzdkM2Y2Y2NmM2FmNWM5MjY5NDRmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2019-04-15 20:46:46'),
('6b5kuwl4wrsq2lqaya3zpxii4tse5pq9', 'ZTk2MzU0NDIwYmFiZjA3OTc3OGFlMDg0ZTUxMjE0YjNhZTk3YjI3Zjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxY2IzZDNhYmRlYWZmMWMzNTEzNzQzYWJmNTg5NDEwNTNmZjBjZmNiIn0=', '2020-01-01 18:56:27'),
('6m7pj8ppab5ixidgbajmrc1865bzvskj', 'NTAzMTViZTZmMTdhOTE1NjVmYjAzYjM1Y2MwNzEyY2E5ZTU4NTc0ZTp7ImlkX2NsaWVudCI6IjI2MTc4MTU0IiwiZm9ybV9kZXRhaWxzIjoxLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjhmMTM3MDhiYjA2MjNmM2E5NDExNTY0MTFkMzVjMWYwZGYyNmRkODAiLCJfYXV0aF91c2VyX2lkIjoiMSJ9', '2016-02-26 02:53:28'),
('76wv6xy9e6gyp9rc44ka9abcakpfu3gw', 'YzI2NjM1ODU2M2QyMjljYmRiMzIxNjljM2UxODU0NmFlNzg0MWI4Mjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiaWRfY2xpZW50IjoiMjYxNzgxNTQiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfaGFzaCI6IjhmMTM3MDhiYjA2MjNmM2E5NDExNTY0MTFkMzVjMWYwZGYyNmRkODAiLCJmb3JtX2RldGFpbHMiOjF9', '2016-02-25 19:40:49'),
('7bhpc1u8kkwyzk86vw6dcke2tedb0n7p', '.eJxVjMEOwiAQRP-FsyFAKywevfsNZNkFqRpISnsy_rtt0oNeJpl5M_MWAdelhLWnOUwsLgLE6TeLSM9Ud8APrPcmqdVlnqLcK_KgXd4ap9f16P4dFOxlW3vlbWICfQZUEZx3YNiMA-Ts0UKmETlak1VGtOT0pjr5zdPAySCKzxfqDzig:1r3bwg:NMqQvQIsY6G5why6Gtgl3Yvo2rHn-mmTM9RjQzfTEQM', '2023-11-30 12:58:10'),
('7msqmlq5x95pimhzae0zin7z34dccazs', 'YzlkMTU4MmNiZjU4MWI2NTRlZWMwMDZlNmI1YTI3Y2EyZjRhYzU5Mzp7ImZvcm1fZGV0YWlscyI6MiwiaWRfY2xpZW50IjoiMjYxNzgxNTQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9', '2016-02-25 17:48:31'),
('81od7x45rebmf9ljnwf91gks0r4rtb1g', 'OTVkYWVhZWVlNTI5ZDM4N2JhZDFmNTkxMGFkY2UwM2VhYmM3NjZiMDp7ImZvcm1fZGV0YWlscyI6MSwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjhmMTM3MDhiYjA2MjNmM2E5NDExNTY0MTFkMzVjMWYwZGYyNmRkODAiLCJpZF9jbGllbnQiOiIyNjE3ODE1NCJ9', '2016-02-25 16:38:03'),
('8htql1esl991b8gt2t4cdy2o45efiafe', '.eJxVjMEOwiAQRP-FsyFAKywevfsNZNkFqRpISnsy_rtt0oNeJpl5M_MWAdelhLWnOUwsLgLE6TeLSM9Ud8APrPcmqdVlnqLcK_KgXd4ap9f16P4dFOxlW3vlbWICfQZUEZx3YNiMA-Ts0UKmETlak1VGtOT0pjr5zdPAySCKzxfqDzig:1r3l4l:yk_2lWE9R7dMxFnQENpBkPZEtWh66SCvgQA9bKXa424', '2023-11-30 22:43:07'),
('8z8kprv7oq8erd0pktyonbbdh9h3n5wl', 'YTU2MTZkMzhlNjY0NDc0M2NkYWE2NjM2MzVlNjVhMDIyNTZlZjg0Zjp7InByb2R1Y3Rvc0V4cG9ydGFkb3MiOmZhbHNlLCJmb3JtX2RldGFpbHMiOjIsIl9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiOGYxMzcwOGJiMDYyM2YzYTk0MTE1NjQxMWQzNWMxZjBkZjI2ZGQ4MCIsImNsaWVudGVzRXhwb3J0YWRvcyI6ZmFsc2UsImlkX2NsaWVudCI6IjI0NTYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9', '2019-05-19 00:52:40'),
('9us6vieqo4p5zpiek0otcfkcyrbkol00', 'OTViNDQ4NDIxNGFlOTEwOWNiZjA4ZDViNzU0ZWUyYzFhMGY1MWFhMzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwicHJvZHVjdG9Cb3JyYWRvIjpmYWxzZSwicHJvZHVjdG9JRCI6MTksInByb2R1Y3RvUHJvY2VzYWRvIjoiYWdyZWdhZG8iLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjhmMTM3MDhiYjA2MjNmM2E5NDExNTY0MTFkMzVjMWYwZGYyNmRkODAifQ==', '2019-05-12 20:40:00'),
('a1a2n3wql5vi9frpiexs83kfhsxnhjam', 'Y2ZjMGYzNGNkMzMyZjAxMTMyZmJlZjUzNDNjYjIxZDBiYjlkOGVlZDp7Il9hdXRoX3VzZXJfaGFzaCI6IjhmMTM3MDhiYjA2MjNmM2E5NDExNTY0MTFkMzVjMWYwZGYyNmRkODAiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2016-02-26 00:05:03'),
('aiol70jdiy005lss3ftcdthplsbcwi30', 'YjJkYTAwMTI0ODI1OTBkYTZmN2M1Zjc4NjNhZDExZjBiNmEzODU0Yjp7ImZvcm1fZGV0YWlscyI6MSwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwiaWRfY2xpZW50IjoiMjYxNzgxNTQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9', '2016-02-26 02:40:04'),
('avgps3ylmtt8rt23hg76cve3m7elpdic', 'ZDdjNmFiNTk1Nzc1Y2RhODFlMGEzM2JjMjY4NGM3MzZlYTM5OGYwMDp7Il9hdXRoX3VzZXJfaGFzaCI6IjFjYjNkM2FiZGVhZmYxYzM1MTM3NDNhYmY1ODk0MTA1M2ZmMGNmY2IiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIiwicHJvdmVlZG9yUHJvY2VzYWRvIjoiZWRpdGFkbyJ9', '2019-12-10 01:27:38'),
('bdgcelry33olucranpz12cksjwuxrar9', 'NDdhY2ZiODAzMWFkMzY3MWRlYzdkM2Y2Y2NmM2FmNWM5MjY5NDRmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2019-03-30 21:12:19'),
('bqhrsrf5qpj94p5qqsriuz5efsl22csy', 'NjVhY2Q0ZGU0ZTIyNTk1MzU1MTliY2RhNjcxNjRjMzhkMzRhZDQxZTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJpZF9jbGllbnQiOiIyNTIxIiwiZm9ybV9kZXRhaWxzIjoyLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2019-05-19 16:20:47'),
('bx3a7evtef6gxmbrrkgmry0j4z5fc4cw', 'NjJiY2M4ZDgwMTU2M2E1OWEyN2U0ZGFmZjdiMWJhZmQxY2EzZTA2NDp7ImNsaWVudGVQcm9jZXNhZG8iOiJlZGl0YWRvIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJwcm9kdWN0b3NFeHBvcnRhZG9zIjpmYWxzZX0=', '2019-05-16 00:29:36'),
('c7f1f6jrxvwtfpht63md3vrun7vwo4yb', 'NDdhY2ZiODAzMWFkMzY3MWRlYzdkM2Y2Y2NmM2FmNWM5MjY5NDRmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2019-04-14 00:58:30'),
('cr9spe2ny0uv2j2xdwg61xbp4dujbfzh', 'Y2Y3NjczZDBmOTc1YTBlNjhlNTczMWU5YzdmYjVhNzc2YTYwNzlmZDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwiZm9ybV9kZXRhaWxzIjoyLCJpZF9jbGllbnQiOiIyNTg3OTA0MSJ9', '2019-04-20 23:59:47'),
('ctkbu7dkjfvbem9xnk7pg551m0gyig1a', 'NWFkZWYyNWM0NWYxZmU5ZWNkMWFkNDAxNzFjYzU0MTgyOTU3YmFhMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4YjczZTYyY2FiYzM3NGFlNjM2NTU4ZDVjZDFiZWMyYWUxZDBkYjFiIiwicGVyZmlsUHJvY2VzYWRvIjp0cnVlfQ==', '2020-06-23 21:05:29'),
('dapbixceyen9yhcv7bbwoo5f3g2nxlss', 'MTMwNzgxOTMxMDQ3YzAwMzYyNGEwOTVmOGVmMDJhYTU5MzMzMDQzYTp7ImZvcm1fZGV0YWlscyI6MiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJpZF9jbGllbnQiOiIyNjE3ODE1NCIsIl9hdXRoX3VzZXJfaGFzaCI6IjhmMTM3MDhiYjA2MjNmM2E5NDExNTY0MTFkMzVjMWYwZGYyNmRkODAiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9', '2016-02-25 20:57:39'),
('dd8yvmxiy7jc8z3nwaualsukyojjrw72', 'NjliMTc3Nzc5ZDJhNDFiMzFhMGJlNzVlYTczZWQyMDU1ZDk5M2Q4Nzp7ImZvcm1fZGV0YWlscyI6MiwiaWRfY2xpZW50IjoiMjYxNzgxNTQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjhmMTM3MDhiYjA2MjNmM2E5NDExNTY0MTFkMzVjMWYwZGYyNmRkODAiLCJfYXV0aF91c2VyX2lkIjoiMSJ9', '2016-02-25 18:51:54'),
('dm9brzo6dwejaa9nau82on5oq5yqokzu', 'ZGNlOWYxMmJlMzM2NDU3MGFhOTFlMTA2Yzc4YjA4N2VkODE5YzkyZjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiIxY2IzZDNhYmRlYWZmMWMzNTEzNzQzYWJmNTg5NDEwNTNmZjBjZmNiIn0=', '2019-09-19 07:30:17'),
('duddqj4i3s8qrktes6nkfpveop26hcqb', 'N2UwYzhhNzZhOWJmM2U2NGNiOTU1YjQwNDkxYjU1YTQxNGU3ZGFjNjp7ImZvcm1fZGV0YWlscyI6MiwiX2F1dGhfdXNlcl9oYXNoIjoiOGYxMzcwOGJiMDYyM2YzYTk0MTE1NjQxMWQzNWMxZjBkZjI2ZGQ4MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJpZF9jbGllbnQiOiIyNjE3ODE1NCJ9', '2016-02-25 22:53:10'),
('dwfaap4kfln9h878alscuddqt25n9o54', 'NmI2NWU1MmM4YjlkMDdkZWRiZTk4NGM2ZjQ0NmQ5ZTJjMTllZmI0OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwicHJvZHVjdG9Qcm9jZXNhZG8iOmZhbHNlLCJwcm9kdWN0b0lEIjoyNCwicHJvZHVjdG9Cb3JyYWRvIjpmYWxzZX0=', '2019-05-10 23:17:17'),
('e08s9agdkigf565vfv4yuwhvoreuf8xb', 'ZTEyM2ViMTBlMjNmNGU4MzU3MGE3MGQ2MDA4OTQxMjAxNTY5MWE0NTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhmMTM3MDhiYjA2MjNmM2E5NDExNTY0MTFkMzVjMWYwZGYyNmRkODAiLCJmb3JtX2RldGFpbHMiOjEsImlkX2NsaWVudCI6IjI2MTc4MTU0IiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJpZF9wcm92ZWVkb3IiOiIyNjE3ODE2NCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2016-02-26 02:37:59'),
('e39qgh2i1905awumorczqd25mor8ts5i', 'ZDU0MTZmMjhjZGYwMTQyMGI4ODhjYmJjMjRlYTRjM2JhMzgyNTg5NTp7ImlkX3Byb3ZlZWRvciI6IjI2NTQ3ODkyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfaGFzaCI6IjFjYjNkM2FiZGVhZmYxYzM1MTM3NDNhYmY1ODk0MTA1M2ZmMGNmY2IiLCJwcm9kdWN0b1Byb2Nlc2FkbyI6ImFncmVnYWRvIiwiaWRfY2xpZW50IjoiOTk1Njc4MjEiLCJmb3JtX2RldGFpbHMiOjJ9', '2019-12-01 19:44:47'),
('ejdig5btky07v6xprpztdz30phzj63jl', 'NDdhY2ZiODAzMWFkMzY3MWRlYzdkM2Y2Y2NmM2FmNWM5MjY5NDRmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2019-05-04 19:50:33'),
('epnk82z3hoedegm3v3h42t04o0b2rc13', 'NGU2MWQ1MmQ3MmU4M2Q0YWZjMWRkYmI4NDI2NGY0NTA2OGMwOGY5Yzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOGYxMzcwOGJiMDYyM2YzYTk0MTE1NjQxMWQzNWMxZjBkZjI2ZGQ4MCIsImZvcm1fZGV0YWlscyI6MiwiaWRfY2xpZW50IjoiMjYxNzgxNTQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9', '2016-02-25 16:38:28'),
('ew71n8dwycmbkgvfmh5qclxnb57eb2mo', 'Yjk5OTBjOTE1YTEyMzRkOTYyOWVkMTk2ZjE5ZDE0MzdlMzhlN2JkMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiOGYxMzcwOGJiMDYyM2YzYTk0MTE1NjQxMWQzNWMxZjBkZjI2ZGQ4MCIsInByb2R1Y3Rvc0V4cG9ydGFkb3MiOmZhbHNlLCJjbGllbnRlUHJvY2VzYWRvIjoiYWdyZWdhZG8iLCJwcm9kdWN0b1Byb2Nlc2FkbyI6ImFncmVnYWRvIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQifQ==', '2019-06-25 18:55:05'),
('f6oypl7rflibn61gw6ltgf5b85ceavds', 'NTE5MjNkM2VkNGUyYmY0MzQ5MmRlZjNmMjUzYmU2NWNhNGNhOTBiZTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiaWRfY2xpZW50IjoiMjYxNzgxNTQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJmb3JtX2RldGFpbHMiOjF9', '2016-02-25 17:49:13'),
('f9q3tnvoojzybfngzrn4jm4qyo3csapb', 'MzUzMzFmNGM3ODNjMDgzY2ViOGEyMTdkMjgzYjQ5MDFhN2I3MDJlYTp7ImZvcm1fZGV0YWlscyI6NSwiX2F1dGhfdXNlcl9pZCI6IjEiLCJpZF9jbGllbnQiOiIyNjE3ODE1NCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOGYxMzcwOGJiMDYyM2YzYTk0MTE1NjQxMWQzNWMxZjBkZjI2ZGQ4MCJ9', '2016-02-25 20:25:02'),
('fd5c4y7y2fig8cfe2vp3i61qtjmod207', 'NDdhY2ZiODAzMWFkMzY3MWRlYzdkM2Y2Y2NmM2FmNWM5MjY5NDRmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2019-06-18 19:08:18'),
('fiwxw9tqau2qn8h9ytwa8r46pg0wp4a6', 'MTQ5MmNhYjUyNDMwMjg2OTJhMzliNjlhMDA4NzUxY2ZiOGIwYWY0NDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiZm9ybV9kZXRhaWxzIjoxLCJfYXV0aF91c2VyX2hhc2giOiIxY2IzZDNhYmRlYWZmMWMzNTEzNzQzYWJmNTg5NDEwNTNmZjBjZmNiIiwiaWRfY2xpZW50IjoiOTk1Njc4MjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9', '2019-12-03 13:30:00'),
('fll6k2u7pexn2rjt7kfj1il53fxunku8', 'NDdhY2ZiODAzMWFkMzY3MWRlYzdkM2Y2Y2NmM2FmNWM5MjY5NDRmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2019-04-13 17:17:28'),
('g9ge90hanok1r6hfirx6iexx6fvmuluc', 'NTgyMTc2ZjAyYTI0OGYyMWE3ODRiZGYzYTRhNWM0M2QxMjQwZGI2Zjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiOGYxMzcwOGJiMDYyM2YzYTk0MTE1NjQxMWQzNWMxZjBkZjI2ZGQ4MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2016-02-25 17:14:49'),
('gexprydb9x0erbvrg3fp4r61aqhp8n21', 'NDdhY2ZiODAzMWFkMzY3MWRlYzdkM2Y2Y2NmM2FmNWM5MjY5NDRmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2019-03-31 19:50:07'),
('gq7c8r1mnuvnprmlf351w8jlhgaso7qk', 'NDcwYmE5ZDNhMzZhZTg1ZmNiNDkxN2Q0MGE2MTk2NzY0YzgxYzc1MTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwiZm9ybV9kZXRhaWxzIjo0LCJpZF9jbGllbnQiOiIyMjIxMiJ9', '2019-04-26 12:19:42'),
('gzynusybzypk0fknuxz54swjkwiqmzfn', 'YzlmZjc0NTFjYWUyNTBhOTk0MGI4MDQ2NjUwNzcxMWVjNDFhZTQyNzp7ImlkX2NsaWVudCI6IjI2MTc4MTU0IiwicHJvZHVjdG9Qcm9jZXNhZG8iOiJhZ3JlZ2FkbyIsIl9hdXRoX3VzZXJfaWQiOiIxIiwiZm9ybV9kZXRhaWxzIjoyLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjhmMTM3MDhiYjA2MjNmM2E5NDExNTY0MTFkMzVjMWYwZGYyNmRkODAifQ==', '2016-02-25 21:28:03'),
('h4ix1q09cuinah20epc4b5geo138mqwx', 'MGVjZjMwNDcyNjg3YmE4MmZhZmI3ZjRkYTY1YzgzNWQyMDU2NDM2Yjp7ImZvcm1fZGV0YWlscyI6MSwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwiaWRfY2xpZW50IjoiMjYxNzgxNTQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9', '2019-08-17 21:40:18'),
('hg8i1zflebo6k2kyeme768u4le8pl0oe', 'ZGNlOWYxMmJlMzM2NDU3MGFhOTFlMTA2Yzc4YjA4N2VkODE5YzkyZjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiIxY2IzZDNhYmRlYWZmMWMzNTEzNzQzYWJmNTg5NDEwNTNmZjBjZmNiIn0=', '2019-12-02 21:29:32'),
('hkal066nogoak4mw71ghuyvgqqzvgpxc', 'ZTk2MzU0NDIwYmFiZjA3OTc3OGFlMDg0ZTUxMjE0YjNhZTk3YjI3Zjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxY2IzZDNhYmRlYWZmMWMzNTEzNzQzYWJmNTg5NDEwNTNmZjBjZmNiIn0=', '2019-12-27 14:22:16'),
('hkyjg1f425ogzyxbzjzijo8u2z4w4x49', '.eJxVjMEOwiAQRP-FsyFAKywevfsNZNkFqRpISnsy_rtt0oNeJpl5M_MWAdelhLWnOUwsLgLE6TeLSM9Ud8APrPcmqdVlnqLcK_KgXd4ap9f16P4dFOxlW3vlbWICfQZUEZx3YNiMA-Ts0UKmETlak1VGtOT0pjr5zdPAySCKzxfqDzig:1r3l3p:1qX6ahttxCO8UJVURVj7cSlwPGjRvt9Zclelj50x73M', '2023-11-30 22:42:09'),
('hzxk3qhknfjoy6tw2gtaqj5rohucj3wb', 'ZTk2MzU0NDIwYmFiZjA3OTc3OGFlMDg0ZTUxMjE0YjNhZTk3YjI3Zjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxY2IzZDNhYmRlYWZmMWMzNTEzNzQzYWJmNTg5NDEwNTNmZjBjZmNiIn0=', '2019-12-07 00:24:31'),
('i0h887hqdspqpznaa0shnp4hs3mcmvoo', 'NDdhY2ZiODAzMWFkMzY3MWRlYzdkM2Y2Y2NmM2FmNWM5MjY5NDRmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2019-05-02 00:03:09'),
('i75rrt5fglpiqzfwluzu4pqcn000g6vh', 'NzVlYWIyMTUzYTY2MmMzZjNmNWQ5NmExNGY5MDUzMDIzYjIxM2Y2Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwicHJvZHVjdG9Cb3JyYWRvIjpmYWxzZSwicHJvZHVjdG9Qcm9jZXNhZG8iOmZhbHNlLCJwcm9kdWN0b0lEIjoxOH0=', '2019-05-06 00:54:58'),
('i93zc2e20kuw2wia22h7x7vb5nwgviop', 'Yjc2YjNmOGY4MTJkMWQ5MWExNDVmZWMxYWY2ZTBhNDRjMDNlYmNiNjp7ImlkX2NsaWVudCI6IjI2MTc4MTU0IiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjhmMTM3MDhiYjA2MjNmM2E5NDExNTY0MTFkMzVjMWYwZGYyNmRkODAiLCJmb3JtX2RldGFpbHMiOjF9', '2016-02-25 21:16:43'),
('ip5oz51eeooie4nhzv98n1867wbp5gt8', 'NDdhY2ZiODAzMWFkMzY3MWRlYzdkM2Y2Y2NmM2FmNWM5MjY5NDRmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2019-05-03 23:37:39'),
('itgsdb2m35j78wq31xjqkv3hkv4s13xp', 'NDdhY2ZiODAzMWFkMzY3MWRlYzdkM2Y2Y2NmM2FmNWM5MjY5NDRmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2016-02-25 21:34:00'),
('ivxufr0etyzpddnvggbmu5qja2p45w6i', 'NTE5MjNkM2VkNGUyYmY0MzQ5MmRlZjNmMjUzYmU2NWNhNGNhOTBiZTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiaWRfY2xpZW50IjoiMjYxNzgxNTQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJmb3JtX2RldGFpbHMiOjF9', '2016-02-25 18:11:10'),
('iwte7y05ei1kn1k5tuwjogh12tlqgz8a', 'NGQ1ZGQ1MjY0YTAzZjg0YzJhMDM1NWJlYzg4NWRlZTBhMWI0NmFlYzp7ImlkX2NsaWVudCI6IjI2MTc4MTU0IiwiZm9ybV9kZXRhaWxzIjoxLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiOGYxMzcwOGJiMDYyM2YzYTk0MTE1NjQxMWQzNWMxZjBkZjI2ZGQ4MCJ9', '2016-02-25 17:25:20'),
('j12f1q7qa019ccb3otq1s5ctskd7gxfe', 'NDdhY2ZiODAzMWFkMzY3MWRlYzdkM2Y2Y2NmM2FmNWM5MjY5NDRmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2019-04-30 20:59:04'),
('ke2dawkrrvo325x7xu252som9921je6g', 'NDdhY2ZiODAzMWFkMzY3MWRlYzdkM2Y2Y2NmM2FmNWM5MjY5NDRmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2019-05-02 15:08:57'),
('kg1swlke0lymyadtdb1rgjy72r7kbe47', '.eJxVjE0OgjAQhe_StWmgYGldujfxBmQ6MwXUMKSFlfHuloSFbiZv3s_3Vj1s69hvmVM_kboop06_XgB88rwH9IB5EI0yr2kKeq_oI836JsSv69H9A4yQx7L2lbdM6Oqzgyq4znfOkGkbF6MH6yK2QMGaWEUAi11dbs2-_NgQG4ACXZLQhqvckyBnIClYGBIPu_x8AXeQQ9g:1qx58l:sczCWeJwpFaVWlKOvgn0FxJE30LvEvsEJgxjMwkIKPM', '2023-11-12 12:43:39'),
('l5is8uc1eg91cw3z64e2vrt61gp5w1dc', 'MjA4ZTM4Y2UwZDc4YjdlZDkxMjAwNWRiZjc4ZTNiZDJhZmI1OTQ5Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwiaWRfY2xpZW50IjoiMjYxNzgxNTQiLCJmb3JtX2RldGFpbHMiOjIsImlkX3Byb3ZlZWRvciI6IjI3ODQ0NTMxIn0=', '2016-02-26 02:21:00'),
('l6sh071ewa94dh9ndl8jm38nwhs1x51p', 'YzcwNjM1ODc2Y2Q1MTJkNTc1OGExYzQ1OTExNWFkNmM4Mzk5N2VjNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiaWRfY2xpZW50IjoiMjYxNzgxNTQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjhmMTM3MDhiYjA2MjNmM2E5NDExNTY0MTFkMzVjMWYwZGYyNmRkODAiLCJmb3JtX2RldGFpbHMiOjJ9', '2016-02-25 22:53:16'),
('lh5lyqy0d4p89vpel5wtx3apj9sqowy9', 'MWQyNjRmODY5NWVhNDQzMjhjYzM1MDhiNjFhZDIwNWZhZmFlMTQ0Yzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOGYxMzcwOGJiMDYyM2YzYTk0MTE1NjQxMWQzNWMxZjBkZjI2ZGQ4MCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2016-02-25 17:03:18'),
('lvfkj96xh5gq9hku3ix6vkp5y6czr7q1', 'OTc4MzUxMGNmMmI5MmI0YjdiYTgxZDRkODY2NTBlMTcyYWE0NTk1OTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiZm9ybV9kZXRhaWxzIjoyLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJpZF9jbGllbnQiOiIyNjE3ODE1NCJ9', '2016-02-26 02:28:42'),
('mj2mrasbykpukolasymptnyvw9n4zoyg', 'MGQ0YmI4YjE5NDZjZDE0MGRmYzQ1NjcxMDAxN2VmMGU5NGU3ZDRkYTp7Il9hdXRoX3VzZXJfaGFzaCI6IjFjYjNkM2FiZGVhZmYxYzM1MTM3NDNhYmY1ODk0MTA1M2ZmMGNmY2IiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2016-02-25 20:09:43'),
('mtum45mrcc05helx6v7eqvzn3vm9pyyd', 'NDdhY2ZiODAzMWFkMzY3MWRlYzdkM2Y2Y2NmM2FmNWM5MjY5NDRmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2019-03-31 23:12:23'),
('nq1vl8y1mapu64t11czupbf65wbuzgb9', 'OTcwYmI5NTJiYTNjMzc2ZmRhYmUxN2Q1OWEwYTA3OTIxNGE2Zjg5NDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2016-02-25 16:54:09'),
('nu6k9d40he9nwjmrc16k2s8eumymj9cv', 'MWQyNjRmODY5NWVhNDQzMjhjYzM1MDhiNjFhZDIwNWZhZmFlMTQ0Yzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOGYxMzcwOGJiMDYyM2YzYTk0MTE1NjQxMWQzNWMxZjBkZjI2ZGQ4MCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2016-02-25 17:19:31'),
('o1m4qixje0ck66x3m6cvghg81kj091z0', 'NDdhY2ZiODAzMWFkMzY3MWRlYzdkM2Y2Y2NmM2FmNWM5MjY5NDRmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2019-04-14 22:01:28'),
('p0179nzm48v5cg5l66o4om515bkmwctn', '.eJxVjE0OgjAQhe_StWmgYGldujfxBmQ6MwXUMKSFlfHuloSFbiZv3s_3Vj1s69hvmVM_kboop06_XgB88rwH9IB5EI0yr2kKeq_oI836JsSv69H9A4yQx7L2lbdM6Oqzgyq4znfOkGkbF6MH6yK2QMGaWEUAi11dbs2-_NgQG4ACXZLQhqvckyBnIClYGBIPu_x8AXeQQ9g:1qx4Sb:PIlM4Ks9QMIz6-fUBhLSZshkZSSdGpg2eAcr2VZ5oqQ', '2023-11-12 12:00:05'),
('pd2nv4t9cgloib2lmd614z4j0aore1h2', 'N2M2NDAyNzQ1MzcyMzlmZDM2MzU2YTQyOTM0MzVkN2NiMjIyMjgwNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiaWRfY2xpZW50IjoiMjYxNzgxNTQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwiZm9ybV9kZXRhaWxzIjoxLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9', '2016-02-26 02:39:23'),
('pejrm8jsb3awrz1j77kf7n4fkdt0cmrr', 'NzMxZTM5OWIyNjUzZjQwNzg2MDZiYzJhMjc0NmE5MDY4N2QwNGFkNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwiZm9ybV9kZXRhaWxzIjoxLCJpZF9jbGllbnQiOiIyNTE3ODE2NCJ9', '2019-04-23 17:52:45'),
('phjty2elb240ix3bqkcjhbntn8kbe7gs', 'ZjlmMDMwMjdkYjUwODU5Nzk0NWY2NzFhMGE3M2I5NmQ5OGU5M2RhYTp7Il9hdXRoX3VzZXJfaGFzaCI6IjFjYjNkM2FiZGVhZmYxYzM1MTM3NDNhYmY1ODk0MTA1M2ZmMGNmY2IiLCJpZF9wcm92ZWVkb3IiOiI4NTQxOTQzMiIsImZvcm1fZGV0YWlscyI6MSwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9', '2019-12-03 01:21:14'),
('pmbgf2mg0ynxmfu83ktg8gcy4bk1wrrw', 'Y2ZjMGYzNGNkMzMyZjAxMTMyZmJlZjUzNDNjYjIxZDBiYjlkOGVlZDp7Il9hdXRoX3VzZXJfaGFzaCI6IjhmMTM3MDhiYjA2MjNmM2E5NDExNTY0MTFkMzVjMWYwZGYyNmRkODAiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2016-02-25 17:02:19'),
('pv5qaldhrfi1h4dp6wd9hi4j04z6wh1w', '.eJxVjMEOwiAQRP-FsyFAKywevfsNZNkFqRpISnsy_rtt0oNeJpl5M_MWAdelhLWnOUwsLgLE6TeLSM9Ud8APrPcmqdVlnqLcK_KgXd4ap9f16P4dFOxlW3vlbWICfQZUEZx3YNiMA-Ts0UKmETlak1VGtOT0pjr5zdPAySCKzxfqDzig:1r3jar:O72hcsYAgBO4Yh4Z2kKH996iw0QO_Y1ppVJ9PoZsVxc', '2023-11-30 21:08:09'),
('py0x06try3tj25nblphx0qg4in5t8pie', 'ZDk2NDczYzNjMTFmZWU3ZTI1NzM4NTZlYWU5YjI0NGYxZWIzNjk4ZTp7fQ==', '2019-03-28 15:52:38'),
('qdbxr10xaymsszo21msuxyny96ipfqh0', 'MGQ0YmI4YjE5NDZjZDE0MGRmYzQ1NjcxMDAxN2VmMGU5NGU3ZDRkYTp7Il9hdXRoX3VzZXJfaGFzaCI6IjFjYjNkM2FiZGVhZmYxYzM1MTM3NDNhYmY1ODk0MTA1M2ZmMGNmY2IiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2016-02-25 16:30:56'),
('qqajxe27ya93xe8f6b83tkfc9rj2t5ov', 'MWQyNjRmODY5NWVhNDQzMjhjYzM1MDhiNjFhZDIwNWZhZmFlMTQ0Yzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOGYxMzcwOGJiMDYyM2YzYTk0MTE1NjQxMWQzNWMxZjBkZjI2ZGQ4MCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2016-02-25 19:18:00'),
('qs5qnhtcebrsgnq5hvluuve14cm9j8rq', 'ZTk2MzU0NDIwYmFiZjA3OTc3OGFlMDg0ZTUxMjE0YjNhZTk3YjI3Zjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxY2IzZDNhYmRlYWZmMWMzNTEzNzQzYWJmNTg5NDEwNTNmZjBjZmNiIn0=', '2016-02-25 21:41:08'),
('rb1t7h7kqvh0hxckzxjq7s9eiu8fv91i', '.eJxVTjkOgzAQ_MvWyMKGmLXL9LwBrXftQBKBxFEh_h4TUSTNSHNqduhoW_tuW-LcDQIeEIpfLRC_4nga8qTxMSmexnUegjoj6nIX1U4S3_cr-zfQ09LntiudjcKob0hlwMY1aMTUFabkyGLimiRYk8pEZLnRGXV0mXMl0RDlUaZ5Bb_nh74uwILXXzTH8QE6sT75:1r5qdG:D6Dk-CBk-QR7Bt_k_-KZeJLgC-tqIaS6VZOLeoHvJtY', '2023-12-06 17:03:22'),
('riijh4w0s0m39kaidop8hjlzaekuhk4m', 'NDdhY2ZiODAzMWFkMzY3MWRlYzdkM2Y2Y2NmM2FmNWM5MjY5NDRmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2019-03-28 16:41:56'),
('rnbtxkpo3hu866s7psb8psxq9jg57s19', 'NDg1NTI2NWRlMmVjNjM5ZTU3NzQ5MzM2ODYxN2EyNDcyOTI4Y2I4ODp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJpZF9jbGllbnQiOiIyNjE3ODE1NCIsIl9hdXRoX3VzZXJfaGFzaCI6IjhmMTM3MDhiYjA2MjNmM2E5NDExNTY0MTFkMzVjMWYwZGYyNmRkODAiLCJmb3JtX2RldGFpbHMiOjJ9', '2016-02-25 18:31:01'),
('rp27ost6nnmxwl5lycyleemyv0vh97cu', 'NDg0NWE0ZWJiZjQ1ZmQxMDdlZWU0ZjcwMjZmNmI3YTlmNmI2ZjgzMjp7ImlkX2NsaWVudCI6IjI2MTc4MTU0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJmb3JtX2RldGFpbHMiOjIsIl9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiOGYxMzcwOGJiMDYyM2YzYTk0MTE1NjQxMWQzNWMxZjBkZjI2ZGQ4MCJ9', '2016-02-25 23:28:04'),
('rs0y5z6k7qc69sezv91qzunhuc7kme8c', 'NDdhY2ZiODAzMWFkMzY3MWRlYzdkM2Y2Y2NmM2FmNWM5MjY5NDRmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2019-03-31 16:56:59'),
('sh8reo7cnq21li7jhm0o2skiazwul2pm', 'MDI4ZjQ2ZGY3ZTI5ZDUxNTk5ZTliZTg5MjIxMTgyMTZjZTUwMTg0Yjp7ImlkX2NsaWVudCI6IjI2MTc4MTU0IiwiX2F1dGhfdXNlcl9oYXNoIjoiOGYxMzcwOGJiMDYyM2YzYTk0MTE1NjQxMWQzNWMxZjBkZjI2ZGQ4MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiZm9ybV9kZXRhaWxzIjoyLCJfYXV0aF91c2VyX2lkIjoiMSJ9', '2016-02-25 17:45:27'),
('slv4abddyjl6gije29b2s2mur3dyanu0', 'MDJkMTM4MzJmOGI2ODE2ODg0NTUwMTc4NWYzZTJiNTQ5ZTcwYjE1Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJpZF9jbGllbnQiOiIyNjE3ODE1NCIsIl9hdXRoX3VzZXJfaGFzaCI6IjhmMTM3MDhiYjA2MjNmM2E5NDExNTY0MTFkMzVjMWYwZGYyNmRkODAiLCJmb3JtX2RldGFpbHMiOjF9', '2016-02-25 21:52:33'),
('te174zf8xk4mz6huolw17lkre5t3j2ap', 'ZDUzNmMxYTBhZmNhNWQwMmU4YTRlNTU2MTg5OWRmZGJkN2M1YzMwODp7ImZvcm1fZGV0YWlscyI6MiwiX2F1dGhfdXNlcl9oYXNoIjoiOGYxMzcwOGJiMDYyM2YzYTk0MTE1NjQxMWQzNWMxZjBkZjI2ZGQ4MCIsImlkX2NsaWVudCI6IjI2MTc4MTU0IiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsImlkX3Byb3ZlZWRvciI6IjI3ODQ0NTMxIn0=', '2016-02-25 21:27:28'),
('ttpweyqpgud848b994j3j4e87ka57ctg', 'YzI2NjM1ODU2M2QyMjljYmRiMzIxNjljM2UxODU0NmFlNzg0MWI4Mjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiaWRfY2xpZW50IjoiMjYxNzgxNTQiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfaGFzaCI6IjhmMTM3MDhiYjA2MjNmM2E5NDExNTY0MTFkMzVjMWYwZGYyNmRkODAiLCJmb3JtX2RldGFpbHMiOjF9', '2016-02-25 19:18:44'),
('twfr1azbluru3lcsazsijy2s691v8fan', 'NTY3MjM3ZTZhN2QyZTA0NmVjZmJhMDk4MWMwOTUwZjQ4OWVlMmI0Yjp7ImZvcm1fZGV0YWlscyI6MiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwiaWRfY2xpZW50IjoiMjYxNzgxNjQ4OSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2016-02-25 18:06:11'),
('tyddsib2l597dez2w2od6iah1n08aqz2', 'MGQ0YmI4YjE5NDZjZDE0MGRmYzQ1NjcxMDAxN2VmMGU5NGU3ZDRkYTp7Il9hdXRoX3VzZXJfaGFzaCI6IjFjYjNkM2FiZGVhZmYxYzM1MTM3NDNhYmY1ODk0MTA1M2ZmMGNmY2IiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2016-02-25 16:39:07'),
('uc9c428eugpxm38v9e5xi9bi7h77jtor', 'MWQyNjRmODY5NWVhNDQzMjhjYzM1MDhiNjFhZDIwNWZhZmFlMTQ0Yzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOGYxMzcwOGJiMDYyM2YzYTk0MTE1NjQxMWQzNWMxZjBkZjI2ZGQ4MCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2016-02-25 16:30:23'),
('uct8pq7oydy6xqtzxtpd8aka7r66q2uv', 'NWQzZmYzZTIwYWQzZDBiMmVhODY1NDkxNDkyYzA0NGExNWQzM2VmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJwcm9kdWN0b1Byb2Nlc2FkbyI6ImFncmVnYWRvIiwiX2F1dGhfdXNlcl9oYXNoIjoiOGYxMzcwOGJiMDYyM2YzYTk0MTE1NjQxMWQzNWMxZjBkZjI2ZGQ4MCJ9', '2016-02-25 18:56:03'),
('ulsobxadc9px5qu964zito8kwqp769tu', '.eJxVjMEOwiAQRP-FsyFAKywevfsNZNkFqRpISnsy_rtt0oNeJpl5M_MWAdelhLWnOUwsLgLE6TeLSM9Ud8APrPcmqdVlnqLcK_KgXd4ap9f16P4dFOxlW3vlbWICfQZUEZx3YNiMA-Ts0UKmETlak1VGtOT0pjr5zdPAySCKzxfqDzig:1r3jxH:lURzv3gFdeENvoFKMYYxXo-GP1RMoOR2mQVejeiE6rs', '2023-11-30 21:31:19'),
('ur4rs375igc2wpbm7a300wfg23bt0kal', 'ZTk2MzU0NDIwYmFiZjA3OTc3OGFlMDg0ZTUxMjE0YjNhZTk3YjI3Zjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxY2IzZDNhYmRlYWZmMWMzNTEzNzQzYWJmNTg5NDEwNTNmZjBjZmNiIn0=', '2019-10-07 23:16:21'),
('uxklugj3s4zklshdm732gjtypp6ss8td', 'ZTk2MzU0NDIwYmFiZjA3OTc3OGFlMDg0ZTUxMjE0YjNhZTk3YjI3Zjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxY2IzZDNhYmRlYWZmMWMzNTEzNzQzYWJmNTg5NDEwNTNmZjBjZmNiIn0=', '2019-12-24 20:28:41'),
('uyk03eqd33aadg5736v4lvz92xvddwxu', 'NzY5NjdkMmNlZGFmMWE0MWNjMjUxNDk1MmY3ZTZkMzRjNTA2ODI1OTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiaWRfcHJvdmVlZG9yIjoiODU0MTk0MzIiLCJfYXV0aF91c2VyX2lkIjoiMSIsImZvcm1fZGV0YWlscyI6MSwicHJvZHVjdG9Qcm9jZXNhZG8iOiJhZ3JlZ2FkbyIsIl9hdXRoX3VzZXJfaGFzaCI6IjFjYjNkM2FiZGVhZmYxYzM1MTM3NDNhYmY1ODk0MTA1M2ZmMGNmY2IiLCJpZF9jbGllbnQiOiI5OTU2NzgyMSJ9', '2019-12-01 02:50:47'),
('v1ge0ar04saime3r8isjm1h36p592y1r', 'NDdhY2ZiODAzMWFkMzY3MWRlYzdkM2Y2Y2NmM2FmNWM5MjY5NDRmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2019-05-11 14:57:03'),
('v56a2prv9p3vmzm2vblsuh3obuc378dn', 'YTU1OGVhMjM0Njg4NTM4ZmQxZGExZDM4ZDI0NTM5ZTg5ZGI2ODYyYTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiMWNiM2QzYWJkZWFmZjFjMzUxMzc0M2FiZjU4OTQxMDUzZmYwY2ZjYiIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2019-10-10 00:22:52'),
('viyqqlqoph3fqv91pxry9bw6lcef70zf', 'MThkNDEwZTA5MGJmZjViY2E3YTM1ZmZlMzM1MjA0YjE0NTViZDFhMDp7InByb3ZlZWRvclByb2Nlc2FkbyI6ImFncmVnYWRvIiwiaWRfcHJvdmVlZG9yIjoiOTk5OTk5OTk5OTk5IiwiZm9ybV9kZXRhaWxzIjoyLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwiaWRfY2xpZW50IjoiMjYxNzgxNjQ4OSIsIl9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQifQ==', '2016-02-26 01:10:56'),
('wosxyx616g6oh64vto1vw0zyu2jh7qlv', 'MWQyNjRmODY5NWVhNDQzMjhjYzM1MDhiNjFhZDIwNWZhZmFlMTQ0Yzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOGYxMzcwOGJiMDYyM2YzYTk0MTE1NjQxMWQzNWMxZjBkZjI2ZGQ4MCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2019-09-02 21:53:18'),
('x1twckj08dv179x171vzmybf7ej7teht', 'Mjc2ZWE3NWU4MTExMTdhNzAwMThhOGQ5NGJiZDgzZDZjYjc5MDI1MDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyNTJjYTNmNjRkZGNhMWRlNzQxMjNiMGFjYWEzNGU4YWYxOGFiY2MyIn0=', '2019-09-08 22:45:00'),
('x39v3a2d72q7yc4r3bnimfnkh3pcd14f', 'NDdhY2ZiODAzMWFkMzY3MWRlYzdkM2Y2Y2NmM2FmNWM5MjY5NDRmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2016-02-25 18:47:01'),
('x3fz9c61mppb2m4tttirqi0y5p384ngu', 'YmU4Y2I2ODQwYmJiNWRiNzQ4NzRiMjJiMTllM2Q1NDZhNTc2NjZkYTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiaWRfY2xpZW50IjoiMjYxNzgxNTQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJmb3JtX2RldGFpbHMiOjF9', '2016-02-25 18:45:50'),
('x60u3554mx4xirls2b5yq6zlm9aoou1w', 'NDdhY2ZiODAzMWFkMzY3MWRlYzdkM2Y2Y2NmM2FmNWM5MjY5NDRmYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIn0=', '2019-05-11 20:34:10'),
('xb96oba1skhbqokq764ngc8roucuul2m', 'YjRiM2Q1YjhiOGE4NWJlYjQ5OGM3Mzc0OGNmNzYyZDI2YTJhYjcyODp7ImlkX2NsaWVudCI6IjI2MTc4MTU0IiwiZm9ybV9kZXRhaWxzIjoyLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjhmMTM3MDhiYjA2MjNmM2E5NDExNTY0MTFkMzVjMWYwZGYyNmRkODAiLCJfYXV0aF91c2VyX2lkIjoiMSJ9', '2016-02-25 16:33:04'),
('xid17r308dvgzsa0kf1hnkwxmmutyoc9', 'NzI0YTVlMzEzZjQ5MmI1YjY1MzljOTMzY2FkZTMwN2NiOGY2ZGJlYjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJmb3JtX2RldGFpbHMiOjEsIl9hdXRoX3VzZXJfaGFzaCI6IjhmMTM3MDhiYjA2MjNmM2E5NDExNTY0MTFkMzVjMWYwZGYyNmRkODAiLCJpZF9jbGllbnQiOiIyNjE3ODE1NCJ9', '2016-02-25 20:13:15'),
('y2ljpyfbtpl8cx76hp9bz7k89xi2rvrc', 'NTgyMTc2ZjAyYTI0OGYyMWE3ODRiZGYzYTRhNWM0M2QxMjQwZGI2Zjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiOGYxMzcwOGJiMDYyM2YzYTk0MTE1NjQxMWQzNWMxZjBkZjI2ZGQ4MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2016-02-25 16:31:42'),
('ygrh77scyl83ophcf0rezfdfd9ruek0w', 'ZGYxMDE3YjQ3M2ZlMTUxMjQ2ZDE1YWVjZmM1ZjE2NjdhM2JmNjlmNTp7Il9hdXRoX3VzZXJfaGFzaCI6IjFjYjNkM2FiZGVhZmYxYzM1MTM3NDNhYmY1ODk0MTA1M2ZmMGNmY2IiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsImlkX3Byb3ZlZWRvciI6Ijg1NDE5NDMyIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJmb3JtX2RldGFpbHMiOjF9', '2016-02-25 17:29:29'),
('z29v3fl9sihqptr7xljxl00jbt8e2ddf', '21-TRIAL-YjAzN2RmZDU0MjIzYjRmMzEyYjFiZWE0MjZmZTg1Mjc3MTllOGNiZTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhmMTM3MDhiYjA2MjNmM2E5NDExNTY0MTFkMzVjMWYwZGYyNmRkODAiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0= 116', '2016-02-25 16:57:32'),
('zmgt070rg6ooniddkyuqzl6tgsnb83ez', 'MDJmZGY4ZmM2NDBiYjk0Yzc3ZmYwMjQyYzQ4MzlmY2JjZWJjMTU2ZTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4ZjEzNzA4YmIwNjIzZjNhOTQxMTU2NDExZDM1YzFmMGRmMjZkZDgwIiwiZm9ybV9kZXRhaWxzIjoyLCJpZF9jbGllbnQiOiIyNXU3NTR5dTYifQ==', '2019-04-19 22:27:46'),
('zv4njgpc4hpnessdhrc5ynquems7sfs4', 'MWQyNjRmODY5NWVhNDQzMjhjYzM1MDhiNjFhZDIwNWZhZmFlMTQ0Yzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOGYxMzcwOGJiMDYyM2YzYTk0MTE1NjQxMWQzNWMxZjBkZjI2ZGQ4MCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2016-02-25 16:31:15');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_cart`
--

CREATE TABLE `inventario_cart` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_cartitem`
--

CREATE TABLE `inventario_cartitem` (
  `id` bigint(20) NOT NULL,
  `quantity` int(10) UNSIGNED NOT NULL CHECK (`quantity` >= 0),
  `cart_id` bigint(20) NOT NULL,
  `product_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_categoria`
--

CREATE TABLE `inventario_categoria` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inventario_categoria`
--

INSERT INTO `inventario_categoria` (`id`, `nombre`, `descripcion`) VALUES
(5, 'meow', 'plop'),
(6, 'Gaseosas', 'coca cola');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_cliente`
--

CREATE TABLE `inventario_cliente` (
  `id` bigint(20) NOT NULL,
  `cedula` varchar(12) NOT NULL,
  `nombre` varchar(40) NOT NULL,
  `apellido` varchar(40) NOT NULL,
  `direccion` varchar(200) NOT NULL,
  `nacimiento` date NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `telefono2` varchar(20) DEFAULT NULL,
  `correo` varchar(100) NOT NULL,
  `correo2` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_detallefactura`
--

CREATE TABLE `inventario_detallefactura` (
  `id` bigint(20) NOT NULL,
  `cantidad` int(11) NOT NULL DEFAULT 0,
  `sub_total` text NOT NULL,
  `id_factura_id` bigint(20) NOT NULL,
  `id_producto_id` bigint(20) NOT NULL,
  `total` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_detallepedido`
--

CREATE TABLE `inventario_detallepedido` (
  `id` bigint(20) NOT NULL,
  `cantidad` int(11) NOT NULL DEFAULT 0,
  `sub_total` text NOT NULL,
  `id_pedido_id` bigint(20) NOT NULL,
  `id_producto_id` bigint(20) NOT NULL,
  `total` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_factura`
--

CREATE TABLE `inventario_factura` (
  `id` bigint(20) NOT NULL,
  `fecha` date NOT NULL,
  `monto_general` text NOT NULL,
  `iva_id` int(11) NOT NULL DEFAULT 0,
  `cliente_id` varchar(12) NOT NULL,
  `sub_monto` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_notificaciones`
--

CREATE TABLE `inventario_notificaciones` (
  `id` bigint(20) NOT NULL,
  `mensaje` text NOT NULL,
  `autor_id` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_opciones`
--

CREATE TABLE `inventario_opciones` (
  `id` bigint(20) NOT NULL,
  `valor_iva` int(11) NOT NULL DEFAULT 0,
  `mensaje_factura` text DEFAULT NULL,
  `nombre_negocio` varchar(25) DEFAULT NULL,
  `moneda` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Volcado de datos para la tabla `inventario_opciones`
--

INSERT INTO `inventario_opciones` (`id`, `valor_iva`, `mensaje_factura`, `nombre_negocio`, `moneda`) VALUES
(1, 16, 'Gracias por preferirnos!', 'Donde el compay', '$');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_pedido`
--

CREATE TABLE `inventario_pedido` (
  `id` bigint(20) NOT NULL,
  `fecha` date NOT NULL,
  `monto_general` text NOT NULL,
  `iva_id` int(11) NOT NULL DEFAULT 0,
  `proveedor_id` varchar(12) NOT NULL,
  `presente` varchar(255) DEFAULT '',
  `sub_monto` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_precioscraping`
--

CREATE TABLE `inventario_precioscraping` (
  `id` bigint(20) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `fuente` varchar(100) NOT NULL,
  `fecha_obtencion` datetime(6) NOT NULL,
  `producto_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_producto`
--

CREATE TABLE `inventario_producto` (
  `id` bigint(20) NOT NULL,
  `descripcion` varchar(40) NOT NULL,
  `precio` text NOT NULL,
  `disponible` int(11) DEFAULT 0,
  `tiene_iva` varchar(255) DEFAULT '',
  `tipo` varchar(20) NOT NULL,
  `codigo_barra` varchar(100) DEFAULT NULL,
  `fecha_introduccion` date NOT NULL,
  `fecha_vencimiento` date NOT NULL,
  `categoria_id` bigint(20) NOT NULL,
  `imagen_codigo` varchar(100) DEFAULT NULL,
  `precio_maximo` decimal(10,2) NOT NULL,
  `precio_minimo` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Volcado de datos para la tabla `inventario_producto`
--

INSERT INTO `inventario_producto` (`id`, `descripcion`, `precio`, `disponible`, `tiene_iva`, `tipo`, `codigo_barra`, `fecha_introduccion`, `fecha_vencimiento`, `categoria_id`, `imagen_codigo`, `precio_maximo`, `precio_minimo`) VALUES
(5, 'Yerba Marolio 1kg', '2311', 1, '1', '1', '', '2023-11-20', '2023-11-27', 5, 'codigos/OIG.jpeg', 32321.00, 1221.00),
(6, 'Leche Sancor 1 L', '789', 2, '1', '1', '', '2023-11-21', '2023-11-21', 5, 'codigos/OIG.png', 0.00, 0.00),
(8, 'Galletitas Oreo', '450', 28, '0', '1', '', '2023-11-22', '2024-11-22', 5, 'codigos/OIG.png', 0.00, 0.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_proveedor`
--

CREATE TABLE `inventario_proveedor` (
  `id` bigint(20) NOT NULL,
  `cedula` varchar(12) NOT NULL,
  `nombre` varchar(40) NOT NULL,
  `apellido` varchar(40) NOT NULL,
  `direccion` varchar(200) NOT NULL,
  `nacimiento` date NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `telefono2` varchar(20) DEFAULT NULL,
  `correo` varchar(100) NOT NULL,
  `correo2` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_usuario`
--

CREATE TABLE `inventario_usuario` (
  `id` bigint(20) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  `username` varchar(80) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `first_name` varchar(40) NOT NULL,
  `last_name` varchar(60) NOT NULL,
  `nivel` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inventario_usuario`
--

INSERT INTO `inventario_usuario` (`id`, `last_login`, `is_superuser`, `is_staff`, `is_active`, `date_joined`, `username`, `password`, `email`, `first_name`, `last_name`, `nivel`) VALUES
(1, '2020-06-09 18:59:58', 1, 1, 1, '2019-03-14 15:29:13', 'superadmin', 'pbkdf2_sha256$120000$9mjuMUsIvrio$lJNJ4AP1AqLGh9z4lTV+NsIaXAuEt5A4Pjc48DUsXa8=', 'correo@correo.com', 'Nombre-Aleatorio', 'Apellido-Aleatorio', 2),
(8, '2023-11-16 22:43:07', 1, 1, 1, '2020-06-09 21:07:40', 'admin', 'pbkdf2_sha256$600000$9psEcPr0qhbrPxs2Vi7VHI$edZ3MbSvibpof9oVG5bpGuhUUcrd7pcM9FfQYBy7uJQ=', 'correocualquiera@correo.com', 'nombre', 'apellido', 1),
(9, NULL, 1, 1, 1, '2023-11-16 22:57:14', 'carancho', 'plop', 'mine@hotmail.com', 'Enrique', 'Estes', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_usuario_groups`
--

CREATE TABLE `inventario_usuario_groups` (
  `id` int(11) NOT NULL,
  `usuario_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_usuario_user_permissions`
--

CREATE TABLE `inventario_usuario_user_permissions` (
  `id` int(11) NOT NULL,
  `usuario_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  ADD KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  ADD KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `inventario_cart`
--
ALTER TABLE `inventario_cart`
  ADD PRIMARY KEY (`id`),
  ADD KEY `inventario_cart_user_id_9df1cfb0_fk_inventario_usuario_id` (`user_id`);

--
-- Indices de la tabla `inventario_cartitem`
--
ALTER TABLE `inventario_cartitem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `inventario_cartitem_cart_id_2a76188a_fk_inventario_cart_id` (`cart_id`),
  ADD KEY `inventario_cartitem_product_id_5ab44364_fk_inventari` (`product_id`);

--
-- Indices de la tabla `inventario_categoria`
--
ALTER TABLE `inventario_categoria`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `inventario_cliente`
--
ALTER TABLE `inventario_cliente`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `inventario_detallefactura`
--
ALTER TABLE `inventario_detallefactura`
  ADD PRIMARY KEY (`id`),
  ADD KEY `inventario_detallefactura_id_factura_id_29222149` (`id_factura_id`),
  ADD KEY `inventario_detallefactura_id_producto_id_32c41cd9` (`id_producto_id`);

--
-- Indices de la tabla `inventario_detallepedido`
--
ALTER TABLE `inventario_detallepedido`
  ADD PRIMARY KEY (`id`),
  ADD KEY `inventario_detallepedido_id_pedido_id_810705ef` (`id_pedido_id`),
  ADD KEY `inventario_detallepedido_id_producto_id_4a37bff1` (`id_producto_id`);

--
-- Indices de la tabla `inventario_factura`
--
ALTER TABLE `inventario_factura`
  ADD PRIMARY KEY (`id`),
  ADD KEY `inventario_factura_iva_id_f4b23fb5` (`iva_id`),
  ADD KEY `inventario_factura_cliente_id_9e4d8671` (`cliente_id`);

--
-- Indices de la tabla `inventario_notificaciones`
--
ALTER TABLE `inventario_notificaciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `inventario_notificaciones_autor_id_9d78e0a5` (`autor_id`);

--
-- Indices de la tabla `inventario_opciones`
--
ALTER TABLE `inventario_opciones`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `inventario_pedido`
--
ALTER TABLE `inventario_pedido`
  ADD PRIMARY KEY (`id`),
  ADD KEY `inventario_pedido_iva_id_cd6261ab` (`iva_id`),
  ADD KEY `inventario_pedido_proveedor_id_42fa3e3c` (`proveedor_id`);

--
-- Indices de la tabla `inventario_precioscraping`
--
ALTER TABLE `inventario_precioscraping`
  ADD PRIMARY KEY (`id`),
  ADD KEY `inventario_precioscr_producto_id_c207fa49_fk_inventari` (`producto_id`);

--
-- Indices de la tabla `inventario_producto`
--
ALTER TABLE `inventario_producto`
  ADD PRIMARY KEY (`id`),
  ADD KEY `inventario_producto_categoria_id_7033fb47_fk_inventari` (`categoria_id`);

--
-- Indices de la tabla `inventario_proveedor`
--
ALTER TABLE `inventario_proveedor`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `inventario_usuario`
--
ALTER TABLE `inventario_usuario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `inventario_usuario_groups`
--
ALTER TABLE `inventario_usuario_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `inventario_usuario_groups_usuario_id_group_id_57424a96_uniq` (`usuario_id`,`group_id`),
  ADD KEY `inventario_usuario_groups_usuario_id_ab960dfb` (`usuario_id`),
  ADD KEY `inventario_usuario_groups_group_id_15aaa854` (`group_id`);

--
-- Indices de la tabla `inventario_usuario_user_permissions`
--
ALTER TABLE `inventario_usuario_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `inventario_usuario_user_permissions_usuario_id_permission_id_fd7` (`usuario_id`,`permission_id`),
  ADD KEY `inventario_usuario_user_permissions_usuario_id_8f7821df` (`usuario_id`),
  ADD KEY `inventario_usuario_user_permissions_permission_id_a88ddacb` (`permission_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=81;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT de la tabla `inventario_cart`
--
ALTER TABLE `inventario_cart`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventario_cartitem`
--
ALTER TABLE `inventario_cartitem`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventario_categoria`
--
ALTER TABLE `inventario_categoria`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `inventario_cliente`
--
ALTER TABLE `inventario_cliente`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventario_detallefactura`
--
ALTER TABLE `inventario_detallefactura`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventario_detallepedido`
--
ALTER TABLE `inventario_detallepedido`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventario_factura`
--
ALTER TABLE `inventario_factura`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventario_notificaciones`
--
ALTER TABLE `inventario_notificaciones`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventario_opciones`
--
ALTER TABLE `inventario_opciones`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `inventario_pedido`
--
ALTER TABLE `inventario_pedido`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventario_precioscraping`
--
ALTER TABLE `inventario_precioscraping`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventario_producto`
--
ALTER TABLE `inventario_producto`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `inventario_proveedor`
--
ALTER TABLE `inventario_proveedor`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventario_usuario`
--
ALTER TABLE `inventario_usuario`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `inventario_usuario_groups`
--
ALTER TABLE `inventario_usuario_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventario_usuario_user_permissions`
--
ALTER TABLE `inventario_usuario_user_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk` FOREIGN KEY (`user_id`) REFERENCES `inventario_usuario` (`id`);

--
-- Filtros para la tabla `inventario_cart`
--
ALTER TABLE `inventario_cart`
  ADD CONSTRAINT `inventario_cart_user_id_9df1cfb0_fk_inventario_usuario_id` FOREIGN KEY (`user_id`) REFERENCES `inventario_usuario` (`id`);

--
-- Filtros para la tabla `inventario_cartitem`
--
ALTER TABLE `inventario_cartitem`
  ADD CONSTRAINT `inventario_cartitem_cart_id_2a76188a_fk_inventario_cart_id` FOREIGN KEY (`cart_id`) REFERENCES `inventario_cart` (`id`),
  ADD CONSTRAINT `inventario_cartitem_product_id_5ab44364_fk_inventari` FOREIGN KEY (`product_id`) REFERENCES `inventario_producto` (`id`);

--
-- Filtros para la tabla `inventario_detallefactura`
--
ALTER TABLE `inventario_detallefactura`
  ADD CONSTRAINT `inventario_detallefactura_id_factura_id_29222149_fk` FOREIGN KEY (`id_factura_id`) REFERENCES `inventario_factura` (`id`),
  ADD CONSTRAINT `inventario_detallefactura_id_producto_id_32c41cd9_fk` FOREIGN KEY (`id_producto_id`) REFERENCES `inventario_producto` (`id`);

--
-- Filtros para la tabla `inventario_detallepedido`
--
ALTER TABLE `inventario_detallepedido`
  ADD CONSTRAINT `inventario_detallepedido_id_pedido_id_810705ef_fk` FOREIGN KEY (`id_pedido_id`) REFERENCES `inventario_pedido` (`id`),
  ADD CONSTRAINT `inventario_detallepedido_id_producto_id_4a37bff1_fk` FOREIGN KEY (`id_producto_id`) REFERENCES `inventario_producto` (`id`);

--
-- Filtros para la tabla `inventario_precioscraping`
--
ALTER TABLE `inventario_precioscraping`
  ADD CONSTRAINT `inventario_precioscr_producto_id_c207fa49_fk_inventari` FOREIGN KEY (`producto_id`) REFERENCES `inventario_producto` (`id`);

--
-- Filtros para la tabla `inventario_producto`
--
ALTER TABLE `inventario_producto`
  ADD CONSTRAINT `inventario_producto_categoria_id_7033fb47_fk_inventari` FOREIGN KEY (`categoria_id`) REFERENCES `inventario_categoria` (`id`);

--
-- Filtros para la tabla `inventario_usuario_groups`
--
ALTER TABLE `inventario_usuario_groups`
  ADD CONSTRAINT `inventario_usuario_groups_usuario_id_ab960dfb_fk` FOREIGN KEY (`usuario_id`) REFERENCES `inventario_usuario` (`id`);

--
-- Filtros para la tabla `inventario_usuario_user_permissions`
--
ALTER TABLE `inventario_usuario_user_permissions`
  ADD CONSTRAINT `inventario_usuario_user_permissions_usuario_id_8f7821df_fk` FOREIGN KEY (`usuario_id`) REFERENCES `inventario_usuario` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
