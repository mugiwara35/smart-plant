"""
URL configuration for smartplant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.utamaView, name='utama'),
    path('login/',  include(('akun.urls', 'akun'), namespace='akun')),
    path('alat/', include(('alat.urls', 'alat'), namespace='alat')),
    path('tanaman/', include(('tanaman.urls', 'tanaman'), namespace='tanaman')),
    path('wadah_air/', include(('wadah_air.urls', 'wadah_air'), namespace='wadah_air')),
    path('pompa/', include(('pompa.urls', 'pompa'), namespace='pompa')),
    path('panen/', include(('panen.urls', 'panen'), namespace='panen')),
]
