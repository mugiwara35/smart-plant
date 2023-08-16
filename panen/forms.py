from django import forms
from . import models

class panenForm(forms.ModelForm):
    class Meta:
        model = models.PANEN
        fields = [
            'suhu', 'jumlah_air', 'kelembapan'
        ]
        labels = {
            'jumlah_air': 'Jumlah Air',
        }
        widgets = {
            'suhu': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Masukkan rata-rata suhu',
                    'autocomplete':'off',
                    'type': 'number',
                }
            ),
            'jumlah_air': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Masukkan rata-rata jumlah air',
                    'autocomplete':'off',
                    'type': 'number',
                }
            ),
            'kelembapan': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'asukkan rata-rata kelembapan',
                    'autocomplete':'off',
                    'type': 'number',
                }
            ),
        }