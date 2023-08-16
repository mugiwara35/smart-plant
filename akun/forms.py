from django import forms
from django.contrib.auth.models import User
from . import models


class loginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control input-field',
                'placeholder':'Masukkan username anda',
                'autocomplete':'off',
            }
        )
    )
    password = forms.CharField(
        label="Password",
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-field',
                'placeholder':'Masukkan password anda',
                'type':'password',
                'autocomplete':'off',
                
            }
        )
    )
    
class userForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control input-field',
                'placeholder':'Masukkan username anda',
                'autocomplete':'off',
            }
        )
    )
    password = forms.CharField(
        label="Password",
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-field',
                'placeholder':'Masukkan password anda',
                'type':'password',
                'autocomplete':'off',
                
            }
        )
    )
    
    password_validasi = forms.CharField(
        label="Validasi Password",
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-field',
                'placeholder':'validasi password',
                'type':'password',
                'autocomplete':'off',
                
            }
        )
    )
    
class akunForm(forms.ModelForm):
    class Meta:
        model = models.AKUN
        fields = [
            'nama',
        ]
        labels = {
            'nama': 'Nama Anda',
        }
        widgets = {
            'nama': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Masukkan Nama Anda',
                    'autocomplete':'off',
                }
            )
        }
        
class update_userForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
        ]
        labels = {
            'username': 'Username',
        }
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Masukkan Username Anda',
                    'autocomplete':'off',
                }
            )
        }

class update_passworForm(forms.Form):
    password_lama = forms.CharField(
        label="Password Lama",
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-field',
                'placeholder':'Masukkan password lama anda',
                'type':'password',
                'autocomplete':'off',
                
            }
        )
    )
    
    password_baru = forms.CharField(
        label="Password Baru",
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-field',
                'placeholder':'Masukkan password baru anda',
                'type':'password',
                'autocomplete':'off',
                
            }
        )
    ) 
        
        