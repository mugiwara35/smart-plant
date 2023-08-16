from django import forms
from django.forms import ModelChoiceField

from . import models
from pompa.models import POMPA

class pompaChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.alat.nama_alat} - {obj.nama_pompa}'

class tanamanForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(tanamanForm,self).__init__(*args, **kwargs)
        self.fields['pompa'] = pompaChoiceField(
            widget=forms.Select(
                attrs={
                    'id':'pompaField',
                    'class':'form-select form-select-md',
                }
            ),
            queryset=POMPA.objects.filter(alat__akun__user=user),
            required=False,
        )
        
    class Meta:
        model = models.TANAMAN
        fields = [
            'pompa', 'nama_tanaman', 'keterangan', 'min_kelembapan', 'mode','tanggal_menanam',
        ]
        labels = {
            'nama_tanaman': 'Nama Tanaman',
            'tanggal_menanam': 'Tanggal Menanam',
            'min_kelembapan': 'Minimal Kelembapan',
            'mode': 'Mode Penyiraman Berdasarkan',
        }
        widgets = {
            'pompa': forms.Select(
                attrs={
                    'id':'pompaField',
                    'class':'form-select form-select-md', 
                }
            ),
            
            'nama_tanaman': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Masukkan Nama Tanaman',
                    'autocomplete':'off',
                }
            ),
            
            'keterangan': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Masukkan Keterangan Mengenai Tanaman Anda',
                    'autocomplete':'off',
                }
            ),
            'min_kelembapan': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Masukkan Nilai Minimal Kelembapan',
                    'autocomplete':'off',
                    'type': 'number',
                }
            ),
            'mode': forms.RadioSelect(
                attrs={
                    'id': 'modeRadio',
                    'class': 'form-check-input',
                }
            ),
            'tanggal_menanam': forms.DateInput(
                attrs={
                    'id': 'tanggal_menanam',
                    'class':'form-control dateselect',
                    'autocomplete': 'off',
                }
            ),
        }
        
class penjadwalanForm(forms.ModelForm):
    class Meta:
        model = models.PENJADWALAN
        fields = [
            'jam', 'menit', 'lama_menyiram'
        ]
        labels = {
            'jam': 'Jam(1-24)',
            'menit': 'Menit(0-59)',
            'lama_menyiram': 'Lamanya Pompa Menyala(Menit)',
        }
        widgets = {
            # 'waktu_menyiram': forms.TimeInput(
            #     attrs={
            #         'id':'waktu_menyiramField', 
            #         'class': 'form-control',
            #     },
            # ),
            'jam': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Masukkan jam',
                    'autocomplete':'off',
                    'type': 'number',
                }
            ),
            'menit': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Masukkan menit',
                    'autocomplete':'off',
                    'type': 'number',
                }
            ),
            'lama_menyiram': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Masukkan lamanya pompa akan menyala(menit)',
                    'autocomplete':'off',
                    'type': 'number',
                }
            ),
        }