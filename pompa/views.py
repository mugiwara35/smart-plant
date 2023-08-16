from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import POMPA
from .forms import pompaForm
from datetime import datetime


@csrf_exempt
def pompa_listView(request): 
    context = {
        'page_title': 'Pompa Anda',
        'heading': 'List Pompa Anda',
        'nav_menu': 'nav_pompa',
    }
    if request.method == "GET":
        print('get')
        if not request.user.is_authenticated:
            return redirect('/login/')
        else:
            pompa = POMPA.objects.filter(alat__akun__user=request.user)
            context.update({
                'pompa': pompa,
            })
    elif request.method == "POST":
        if 'ubah' in request.POST:
            request.session['pompa_ubah_dipilih'] = int(request.POST.get('ubah'))
            return redirect('pompa:pompa_ubah')
        elif 'hapus' in request.POST:
            print('hapus')
            pompa = POMPA.objects.get(id=int(request.POST.get('hapus')))
            pompa.delete()
            request.session['pompa_hapus_berhasil'] = 'berhasil'
            return redirect('pompa:pompa_hapus_berhasil')
        
    return render(request, 'pompa/pompa_list.html', context)


@csrf_exempt
def pompa_tambahView(request):
    pompa_form = pompaForm(request.user, request.POST or None)
    context = {
        'page_title': 'Tambah Pompa',
        'heading': 'Tambah Pompa',
        'nav_menu': 'nav_pompa',
        'pompa_form': pompa_form,
    }
    
    if request.method == "GET":
        print("GET")
        if not request.user.is_authenticated:
            return redirect('utama')
            
    elif request.method == "POST":
        print("POST")
        if 'tambah' in request.POST:
            if pompa_form.is_valid():
                pompa = POMPA.objects.create(
                    alat = pompa_form.cleaned_data.get('alat'),
                    wadah_air = pompa_form.cleaned_data.get('wadah_air'),
                    nama_pompa = pompa_form.cleaned_data.get('nama_pompa'),
                )
                if pompa.pk:
                    print('berhasil tambah')
                    request.session['pompa_tambah_berhasil'] = 'berhasil'
                    return redirect('pompa:pompa_tambah_berhasil')
                else:
                    print('gagal tambah')
            else:
                print('tidak valid')
        
    return render(request, 'pompa/pompa_tambah.html', context)

def pompa_ubahView(request):
    if not 'pompa_ubah_dipilih' in request.session and not request.user.is_authenticated:
        return redirect('utama')    
    pompa = POMPA.objects.get(id=request.session['pompa_ubah_dipilih'])
    context = {
        'page_title': 'Ubah Pompa',
        'heading': 'Ubah Pompa',
        'nav_menu': 'nav_pompa',
    }
    
    if request.method == "GET":
        print("GET")
        
        data_pompa = {
            'alat': pompa.alat,
            'wadah_air': pompa.wadah_air,
            'nama_pompa': pompa.nama_pompa,
        }
        pompa_form = pompaForm(request.user, initial=data_pompa, instance=pompa)

        context.update({
            'pompa_form': pompa_form,
        })
            
    elif request.method == "POST":
        print("POST")
        pompa_form = pompaForm(request.user, request.POST or None, instance=pompa)

        context.update({
            'pompa_form': pompa_form,
        })
            
        if 'simpan' in request.POST:
            if pompa_form.is_valid():
                print('berhasil pompa')
                pompa_form.save()
                request.session['pompa_ubah_berhasil'] = 'berhasil'
                return redirect('pompa:pompa_ubah_berhasil')  
            else:
                print('tidak valid')
        
    return render(request, 'pompa/pompa_ubah.html', context)


class berhasilView(View):
    
    template_name = 'pompa/berhasil.html'
    aksi = None
    context = {}
    
    def get(self, request, *args, **kwargs):
        print('get')
        if not 'pompa_tambah_berhasil' in request.session and not 'pompa_ubah_berhasil' in request.session and not 'pompa_hapus_berhasil' in request.session:
            return redirect('utama')
        else:
            if self.aksi == 'pompa_tambah_berhasil':
                self.context.update({
                    'page_title': 'Tambah Pompa Berhasil',
                    'heading': 'Proses Menambahkan Pompa Berhasil',
                    'body': 'Proses menambahkan Pompa telah berhasil. Silahkan tekan tombol kembali untuk pergi ke halaman pompa',
                })
            elif self.aksi == 'pompa_ubah_berhasil':
               self.context.update({
                    'page_title': 'Update Pompa Berhasil',
                    'heading': 'Proses Menyimpan Perubahan Pompa Anda Berhasil',
                    'body': 'Proses menyimpan perubahan pada pompa anda berhasil disimpan. Silahkan tekan tombol kembali untuk pergi ke halaman pompa',
                }) 
            elif self.aksi == 'pompa_hapus_berhasil':
               self.context.update({
                    'page_title': 'Update Pompa Berhasil',
                    'heading': 'Proses Menyimpan Perubahan Pompa Anda Berhasil',
                    'body': 'Proses menghapus data pompa anda berhasil. Silahkan tekan tombol kembali untuk pergi ke halaman pompa',
                }) 
        return render(request, self.template_name, self.context)