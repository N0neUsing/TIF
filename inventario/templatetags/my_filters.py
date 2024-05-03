from django import template
from datetime import datetime
from decimal import Decimal

register = template.Library()

@register.filter
def is_near_expiry(expiry_date):
    if not expiry_date:
        return False
    return 0 < (expiry_date - datetime.today().date()).days <= 30

@register.filter
def is_expired(expiry_date):
    if not expiry_date:
        return False
    return expiry_date < datetime.today().date()

@register.filter
def is_expiring_soon(expiry_date):
    if not expiry_date:
        return False
    return 0 < (expiry_date - datetime.today().date()).days <= 30

@register.filter
def calculate_subtotal(price, quantity):
    return price * quantity

@register.filter(name='divide')
def divide(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return None

@register.filter(name='multiply')
def multiply(value, arg):
    if isinstance(value, Decimal) and isinstance(arg, (int, float, Decimal)):
        # Convertir el argumento a Decimal si es necesario
        factor = Decimal(str(arg))
        return value * factor
    return value  # O manejar el error como prefieras
