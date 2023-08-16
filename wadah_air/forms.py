from django import forms
from django.forms import ModelChoiceField

from . import models



class wadah_airForm(forms.ModelForm):
    class Meta:
        model = models.WADAH_AIR
        fields = [
            'nama_wadah', 'maks_liter'
        ]
        labels = {
            'maks_liter': 'Daya Tampung (liter)',
        }
        widgets = {
            'nama_wadah': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Masukkan Nama Wadah Air',
                    'autocomplete':'off',
                }
            ),
            'maks_liter': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Masukkan Daya Tampung Wadah',
                    'autocomplete':'off',
                    'type': 'number',
                }
            ),
        }