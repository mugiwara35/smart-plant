from django import forms
from django.forms import ModelChoiceField
from . import models
from tanaman.models import TANAMAN

class tanamanChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.nama_tanaman}'

class hasil_panenForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(hasil_panenForm,self).__init__(*args, **kwargs)
        self.fields['tanaman'] = tanamanChoiceField(
            widget=forms.Select(
                attrs={
                    'id':'tanamanField',
                    'class':'form-select form-select-md',
                }
            ),
            queryset=TANAMAN.objects.filter(akun__user=user),
            required=False,
        )
    class Meta:
        model = models.HASIL_PANEN
        fields = [
            'tanaman','jumlah_buah', 'tanggal_panen',
        ]
        labels = {
            'jumlah_buah': 'Jumlah Buah',
            'tanggal_panen': 'Tanggal Panen',
        }

        widgets = {
            'tanaman': forms.Select(
                attrs={
                    'id':'tanamanField',
                    'class':'form-select form-select-md', 
                }
            ),
            'jumlah_buah': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Masukkan rata-rata jumlah air',
                    'autocomplete':'off',
                    'type': 'number',
                }
            ),
            'tanggal_panen': forms.DateInput(
                attrs={
                    'id': 'tanggal_menanam',
                    'class':'form-control dateselect',
                    'autocomplete': 'off',
                }
            ),
        }
        
class panenForm(forms.ModelForm):
    class Meta:
        model = models.PREDIKSI_PANEN
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
        
class prediksi_panenForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(prediksi_panenForm,self).__init__(*args, **kwargs)
        self.fields['tanaman'] = tanamanChoiceField(
            widget=forms.Select(
                attrs={
                    'id':'tanamanField',
                    'class':'form-select form-select-md',
                }
            ),
            queryset=TANAMAN.objects.filter(akun__user=user),
            required=False,
        )
    class Meta:
        model = models.HASIL_PANEN
        fields = [
            'tanaman'
        ]

        widgets = {
            'tanaman': forms.Select(
                attrs={
                    'id':'tanamanField',
                    'class':'form-select form-select-md', 
                }
            ),
        }
        
# class prediksi_panenForm(forms.Form):
#     def __init__(self, user, *args, **kwargs):
#         super(prediksi_panenForm,self).__init__(*args, **kwargs)
#         CHOICES = [('','-------') ,(data.id, data.nama_tanaman) 
#                    for data in TANAMAN.objects.filter(akun__user=user)]
#         self.fields['tanaman'] = forms.ChoiceField(
#             label = "Tanaman Anda",
#             widget=forms.Select(
#                 attrs={
#                     'id': 'tanamanField',
#                     'class': 'form-select form-select-md',
#                 }
#             ),
#             choices=CHOICES,
#             required=False,
#         )
        
#     tanaman = forms.ChoiceField(
#         label = "Tanaman Anda",
#         widget=forms.Select(
#             attrs={
#                 'class': 'form-select form-select-md',
#             }), 
#     )