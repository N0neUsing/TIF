from django import template
from datetime import datetime, timedelta

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

@register.filter
def multiply(value, arg):
    return value * arg
