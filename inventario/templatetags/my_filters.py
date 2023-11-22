from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter(name='is_near_expiry')
def is_near_expiry(expiry_date):
    if not expiry_date:
        return False
    return (expiry_date - datetime.today().date()) <= timedelta(days=15)

@register.filter  # Añade el decorador aquí
def calculate_subtotal(price, quantity):
    return price * quantity

@register.filter
def multiply(value, arg):
    return value * arg