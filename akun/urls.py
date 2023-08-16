from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginView, name='login'),
    path('register/', views.registerView, name='register'),
    path('logout/', views.logoutView, name='logout'),
    path('akun/', views.update_akunView, name='update_akun'),
    path('register/berhasil', views.berhasilView.as_view(aksi='register_berhasil'), name='register_berhasil'),
    path('akun/berhasil', views.berhasilView.as_view(aksi='update_akun_berhasil'), name='update_akun_berhasil'),
]