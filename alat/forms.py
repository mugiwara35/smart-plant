from django import forms

from . import models

class alatForm(forms.ModelForm):
    class Meta:
        model = models.ALAT
        fields = [
            'nama_alat', 'mac_esp', 'ssid',
        ]
        labels = {
            'nama_alat': 'Nama Alat',
            'mac_esp': 'MAC ESP',
            'ssid': 'SSID',
        }
        widgets = {
            'nama_alat': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Masukkan Nama Alat',
                    'autocomplete':'off',
                }
            ),
            'mac_esp': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Masukkan MAC ESP',
                    'autocomplete':'off',
                }
            ),
            'ssid': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Masukkan SSID',
                    'autocomplete':'off',
                }
            ),
        }