from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import WADAH_AIR
from akun.models import AKUN
from .forms import wadah_airForm


# Create your views here.
@csrf_exempt
def wadah_listView(request): 
    context = {
        'page_title': 'Wadah Air Anda',
        'heading': 'List Wadah Air Anda',
        'nav_menu': 'nav_wadah_air',
    }
    if request.method == "GET":
        print('get')
        if not request.user.is_authenticated:
            return redirect('/login/')
        else:
            wadah_air = WADAH_AIR.objects.filter(akun__user=request.user)

            context.update({
                'wadah_air': wadah_air,
            })
    elif request.method == "POST":
        if 'ubah' in request.POST:
            request.session['wadah_air_ubah_dipilih'] = int(request.POST.get('ubah'))
            return redirect('wadah_air:wadah_ubah')
        elif 'hapus' in request.POST:
            print('hapus')
            wadah_air = WADAH_AIR.objects.get(id=int(request.POST.get('hapus')))
            wadah_air.delete()
            request.session['wadah_air_hapus_berhasil'] = 'berhasil'
            return redirect('wadah_air:wadah_hapus_berhasil')
        
    return render(request, 'wadah_air/wadah_list.html', context)

@csrf_exempt
def wadah_tambahView(request):
    wadah_air_form = wadah_airForm(request.POST or None)
    context = {
        'page_title': 'Tambah Wadah Air',
        'heading': 'Tambah Wadah Air',
        'nav_menu': 'nav_wadah_air',
        'wadah_air_form': wadah_air_form,
    }
    
    if request.method == "GET":
        print("GET")
        if not request.user.is_authenticated:
            return redirect('utama')
            
    elif request.method == "POST":
        print("POST")
        if 'tambah' in request.POST:
            if wadah_air_form.is_valid():
                try:
                    akun = AKUN.objects.get(user=request.user)
                    wadah_air = WADAH_AIR.objects.create(
                        akun = akun,
                        nama_wadah = wadah_air_form.cleaned_data.get('nama_wadah'),
                        maks_liter = wadah_air_form.cleaned_data.get('maks_liter'),
                    )
                    if wadah_air.pk:
                        print('berhasil tambah')
                        request.session['wadah_air_tambah_berhasil'] = 'berhasil'
                        return redirect('wadah_air:wadah_tambah_berhasil')
                    else:
                        print('gagal tambah')
                except AKUN.DoesNotExist:
                    print('akun tidak ditemukan')
            else:
                print('tidak valid')
        
    return render(request, 'wadah_air/wadah_tambah.html', context)

def wadah_ubahView(request):
    if not 'wadah_air_ubah_dipilih' in request.session and not request.user.is_authenticated:
        return redirect('utama')    
    wadah_air = WADAH_AIR.objects.get(id=request.session['wadah_air_ubah_dipilih'])
    context = {
        'page_title': 'Ubah Wadah Air',
        'heading': 'Ubah Wadah Air',
        'nav_menu': 'nav_wadah_air',
    }
    
    if request.method == "GET":
        print("GET")
        
        data_wadah_air = {
            'nama_wadah': wadah_air.nama_wadah,
            'maks_liter' : wadah_air.maks_liter,
        }
        wadah_air_form = wadah_airForm(initial=data_wadah_air, instance=wadah_air)

        context.update({
            'wadah_air_form': wadah_air_form,
        })
            
    elif request.method == "POST":
        print("POST")
        wadah_air_form = wadah_airForm(request.POST or None, instance=wadah_air)

        context.update({
            'wadah_air_form': wadah_air_form,
        })
            
        if 'simpan' in request.POST:
            if wadah_air_form.is_valid():
                print('berhasil wadah air')
                wadah_air_form.save()
                request.session['wadah_air_ubah_berhasil'] = 'berhasil'
                return redirect('wadah_air:wadah_ubah_berhasil')  
            else:
                print('tidak valid')
        
    return render(request, 'wadah_air/wadah_ubah.html', context)

class berhasilView(View):
    
    template_name = 'wadah_air/berhasil.html'
    aksi = None
    context = {}
    
    def get(self, request, *args, **kwargs):
        print('get')
        if not 'wadah_air_tambah_berhasil' in request.session and not 'wadah_air_ubah_berhasil' in request.session and not 'wadah_air_hapus_berhasil' in request.session:
            return redirect('utama')
        else:
            if self.aksi == 'wadah_air_tambah_berhasil':
                self.context.update({
                    'page_title': 'Tambah Wadah Air Berhasil',
                    'heading': 'Proses Menambahkan Wadah Air Berhasil',
                    'body': 'Proses menambahkan wadah air telah berhasil. Silahkan tekan tombol kembali untuk pergi ke halaman wadah air',
                })
            elif self.aksi == 'wadah_air_ubah_berhasil':
               self.context.update({
                    'page_title': 'Update Wadah Air Berhasil',
                    'heading': 'Proses Menyimpan Perubahan Wadah Air Anda Berhasil',
                    'body': 'Proses menyimpan perubahan pada wadah air anda berhasil disimpan. Silahkan tekan tombol kembali untuk pergi ke halaman wadah air',
                }) 
            elif self.aksi == 'wadah_air_hapus_berhasil':
               self.context.update({
                    'page_title': 'Update Wadah Air Berhasil',
                    'heading': 'Proses Menyimpan Perubahan Wadah Air Anda Berhasil',
                    'body': 'Proses menghapus data wadah air anda berhasil. Silahkan tekan tombol kembali untuk pergi ke halaman wadah air',
                }) 
        return render(request, self.template_name, self.context)