from django.urls import path
from . import views

urlpatterns = [
    path('', views.panenView, name='panen'),
    path('berhasil_panen/', views.klasifikasiView.as_view(aksi='klasifikasi_panen_berhasil'), name='klasifikasi_berhasil'),
    path('gagal_panen/', views.klasifikasiView.as_view(aksi='klasifikasi_panen_gagal'), name='klasifikasi_gagal'),
    
]