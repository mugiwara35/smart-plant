from django import forms
from tanaman.models import TANAMAN


class filterForm(forms.Form):
    def __init__(self, akun, *args, **kwargs):
        super(filterForm,self).__init__(*args, **kwargs)
        CHOICES = [(data.id, data.nama_tanaman) 
                   for data in TANAMAN.objects.filter(pompa__alat__akun=akun)]
        self.fields['tanaman'] = forms.ChoiceField(
            label = "Tanaman Anda",
            widget=forms.Select(
                attrs={
                    'id': 'tanamanField',
                    'class': 'form-select form-select-md',
                }
            ),
            choices=CHOICES,
        )
        
        
    tanggal_kelembapan = forms.DateField(
        label="Tanggal",
        required=False,
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(
            attrs={
                'id': 'tanggal_kelembapanField',
                'class': 'form-control dateselect',
            }
        ),
    )
    tanaman = forms.ChoiceField(
        label = "Tanaman Anda",
        widget=forms.Select(
            attrs={
                'class': 'form-select form-select-md',
            }), 
    )
    
    