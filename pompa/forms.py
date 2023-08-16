from django import forms
from django.db.models.base import Model
from django.forms import ModelChoiceField

from . import models
from alat.models import ALAT
from wadah_air.models import WADAH_AIR 

class alatChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.nama_alat}'

class wadahChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.nama_wadah}'

class pompaForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(pompaForm,self).__init__(*args, **kwargs)
        print(user)
        self.fields['alat'] = alatChoiceField(
            widget=forms.Select(
                attrs={
                    'id':'alatField',
                    'class':'form-select form-select-md',
                }
            ),
            queryset=ALAT.objects.filter(akun__user=user),
        )
        self.fields['wadah_air'] = wadahChoiceField(
            widget=forms.Select(
                attrs={  
                    'id':'wadah_airField',
                    'class':'form-select form-select-md',
                }
            ),
            queryset=WADAH_AIR.objects.select_related('akun').filter(akun__user=user),
        )

    class Meta:
        model = models.POMPA
        fields = [
            'alat', 'wadah_air', 'nama_pompa', 
        ]
        labels = {
            'wadah_air': 'Wadah Air',
            'nama_pompa': 'Nama Pompa',
        }
        widgets = {
            'alat': forms.Select(
                attrs={
                    'id':'alatField',
                    'class':'form-select form-select-md', 
                }
            ),
            'wadah_air': forms.Select(
                attrs={
                    'id':'wadah_airField',
                    'class':'form-select form-select-md', 
                }
            ),
            'nama_pompa': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Masukkan Nama Pompa',
                    'autocomplete':'off',
                }
            ),
        }