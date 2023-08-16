from django.shortcuts import render,redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import ALAT
from .forms import alatForm
from akun.models import AKUN
from datetime import datetime

# Create your views here.
@csrf_exempt
def alat_listView(request): 
    context = {
        'page_title': 'Alat Anda',
        'heading': 'List Alat Anda',
        'nav_menu': 'nav_alat',
    }
    if request.method == "GET":
        print('get')
        if not request.user.is_authenticated:
            return redirect('/login/')
        else:
            alat = ALAT.objects.filter(akun__user=request.user)
            print(alat)
            context.update({
                'alat': alat,
            })
    elif request.method == "POST":
        if 'ubah' in request.POST:
            request.session['alat_ubah_dipilih'] = int(request.POST.get('ubah'))
            return redirect('alat:alat_ubah')
        elif 'hapus' in request.POST:
            print('hapus')
            alat = ALAT.objects.get(id=int(request.POST.get('hapus')))
            alat.delete()
            request.session['alat_hapus_berhasil'] = 'berhasil'
            return redirect('alat:alat_hapus_berhasil')
        
    return render(request, 'alat/alat_list.html', context)

@csrf_exempt
def alat_tambahView(request):
    alat_form = alatForm(request.POST or None)
    context = {
        'page_title': 'Tambah Alat',
        'heading': 'Tambah Alat',
        'nav_menu': 'nav_alat',
        'alat_form': alat_form,
    }
    
    if request.method == "GET":
        print("GET")
        if not request.user.is_authenticated:
            return redirect('utama')
            
    elif request.method == "POST":
        print("POST")
        if 'tambah' in request.POST:
            if alat_form.is_valid():
                try:
                    akun = AKUN.objects.get(user=request.user)
                    
                    alat = ALAT.objects.create(
                        akun = akun,
                        nama_alat = alat_form.cleaned_data.get('nama_alat'),
                        mac_esp = alat_form.cleaned_data.get('mac_esp'),
                        ssid = alat_form.cleaned_data.get('ssid'),
                        tanggal_aktif = datetime.now(),
                    )
                    if alat.pk:
                        print('berhasil tambah')
                        request.session['alat_tambah_berhasil'] = 'berhasil'
                        return redirect('alat:alat_tambah_berhasil')
                    else:
                        print('gagal tambah')
                except AKUN.DoesNotExist:
                    print('akun tidak ada')
                    return redirect('utama')
            else:
                print('tidak valid')
        
    return render(request, 'alat/alat_tambah.html', context)

def alat_ubahView(request):
    if not 'alat_ubah_dipilih' in request.session and not request.user.is_authenticated:
        return redirect('utama')    
    alat = ALAT.objects.get(id=request.session['alat_ubah_dipilih'])
    context = {
        'page_title': 'Ubah Alat',
        'heading': 'Ubah Alat',
        'nav_menu': 'nav_alat',
    }
    
    if request.method == "GET":
        print("GET")
        
        data_alat = {
            'nama_alat': alat.nama_alat,
            'mac_esp' : alat.mac_esp,
            'ssid' : alat.ssid,
        }
        alat_form = alatForm(initial=data_alat, instance=alat)

        context.update({
            'alat_form': alat_form,
        })
            
    elif request.method == "POST":
        print("POST")
        alat_form = alatForm(request.POST or None, instance=alat)

        context.update({
            'alat_form': alat_form,
        })
            
        if 'simpan' in request.POST:
            if alat_form.is_valid():
                print('berhasil alat')
                alat_form.save()
                request.session['alat_ubah_berhasil'] = 'berhasil'
                return redirect('alat:alat_ubah_berhasil')  
            else:
                print('tidak valid')
        
    return render(request, 'alat/alat_ubah.html', context)

class berhasilView(View):
    
    template_name = 'alat/berhasil.html'
    aksi = None
    context = {}
    
    def get(self, request, *args, **kwargs):
        print('get')
        if not 'alat_tambah_berhasil' in request.session and not 'alat_ubah_berhasil' in request.session and not 'alat_hapus_berhasil' in request.session:
            return redirect('utama')
        else:
            if self.aksi == 'alat_tambah_berhasil':
                self.context.update({
                    'page_title': 'Tambah Alat Berhasil',
                    'heading': 'Proses Menambahkan Alat Berhasil',
                    'body': 'Proses menambahkan alat telah berhasil. Silahkan tekan tombol kembali untuk pergi ke halaman alat',
                })
            elif self.aksi == 'alat_ubah_berhasil':
               self.context.update({
                    'page_title': 'Update Alat Berhasil',
                    'heading': 'Proses Menyimpan Perubahan Alat Anda Berhasil',
                    'body': 'Proses menyimpan perubahan pada alat anda berhasil disimpan. Silahkan tekan tombol kembali untuk pergi ke halaman alat',
                }) 
            elif self.aksi == 'alat_hapus_berhasil':
               self.context.update({
                    'page_title': 'Update Alat Berhasil',
                    'heading': 'Proses Menyimpan Perubahan Alat Anda Berhasil',
                    'body': 'Proses menghapus data alat anda berhasil. Silahkan tekan tombol kembali untuk pergi ke halaman alat',
                }) 
        return render(request, self.template_name, self.context)