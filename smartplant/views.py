from django.shortcuts import render, redirect
from .forms import filterForm
from akun.models import AKUN
from monitoring.models import MONITORING
from datetime import datetime, date

def utamaView(request):
    if request.user.is_authenticated:
        print('sudah login')
        akun = AKUN.objects.get(user=request.user)
        filter_form = filterForm(akun,request.POST or None)
        filter_form.fields['tanggal_kelembapan'].initial = date.today().strftime('%Y-%m-%d')
    
    context = {
        'page_title': 'Smart Plant',
        'nav_menu': 'nav_utama',
    }
    
    if request.method == "GET":
        print('get')
        if not request.user.is_authenticated:
            print('belum login')
        else:    
            monitoring = MONITORING.objects.filter(tanaman__pompa__alat__akun=akun,waktu__contains = date.today())
            filter_form.fields['tanggal_kelembapan'].initial = date.today().strftime('%Y-%m-%d')
            if len(monitoring) > 0:
                monitoring_terakhir = monitoring.latest('waktu')
                print(monitoring_terakhir)
            context.update({
                'filter_form': filter_form, 
                'monitoring': monitoring,
            })
            print(monitoring)
    elif request.method == "POST":
        print('post')
        if 'aksi' in request.POST:
            if request.POST['aksi'] == 'kelembapan_tanaman':
                print('kelembapan_tanaman')
                if filter_form.is_valid():
                    monitoring = MONITORING.objects.filter(tanaman__pompa__alat__akun=akun, tanaman_id=filter_form.cleaned_data.get('tanaman'), waktu__contains = filter_form.cleaned_data.get('tanggal_kelembapan'))
                    if len(monitoring) > 0:
                        monitoring_terakhir = monitoring.latest('waktu')
                        liter_sekarang = monitoring_terakhir.tingkat_air
                        liter_total = monitoring_terakhir.tanaman.pompa.wadah_air.maks_liter
                        liter_digunakan = liter_total - liter_sekarang
                    else:
                        liter_sekarang = 0
                        liter_total = 0
                        liter_digunakan = 0
                    
                    print(liter_sekarang)
                    print(liter_total)
                    print(liter_digunakan)
                    
                    context.update({
                        'filter_form': filter_form, 
                        'monitoring': monitoring,
                        'liter_sekarang': liter_sekarang,
                        'liter_total': liter_total,
                        'liter_digunakan': liter_digunakan,
                    })
                
    return render(request, 'utama.html', context)