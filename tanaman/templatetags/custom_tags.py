from django import template
from tanaman.models import PENJADWALAN

register = template.Library()

@register.filter(name='penjadwalan')
def Penjadwalan(value):
    penjadwalan = PENJADWALAN.objects.filter(tanaman = value)
    return penjadwalan