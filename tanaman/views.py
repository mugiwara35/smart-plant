from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import TANAMAN, PENJADWALAN
from .forms import tanamanForm, penjadwalanForm
from datetime import datetime
from akun.models import AKUN
# Create your views here.

@csrf_exempt
def tanaman_listView(request): 
    context = {
        'page_title': 'Tanaman Anda',
        'heading': 'List Tanaman Anda',
        'nav_menu': 'nav_tanaman',
    }
    if request.method == "GET":
        print('get')
        if not request.user.is_authenticated:
            return redirect('/login/')
        else:
            tanaman = TANAMAN.objects.filter(pompa__alat__akun__user=request.user)
            context.update({
                'tanaman': tanaman,
            })
    elif request.method == "POST":
        if 'ubah' in request.POST:
            request.session['tanaman_ubah_dipilih'] = int(request.POST.get('ubah'))
            return redirect('tanaman:tanaman_ubah')
        elif 'hapus' in request.POST:
            print('hapus')
            tanaman = TANAMAN.objects.get(id=int(request.POST.get('hapus')))
            tanaman.delete()
            request.session['tanaman_hapus_berhasil'] = 'berhasil'
            return redirect('tanaman:tanaman_hapus_berhasil')
        
    return render(request, 'tanaman/tanaman_list.html', context)

@csrf_exempt
def tanaman_tambahView(request):
    tanaman_form = tanamanForm(request.user, request.POST or None)
    penjadwalan_form = penjadwalanForm(request.POST or None)
    context = {
        'page_title': 'Tambah Tanaman',
        'heading': 'Tambah Tanaman',
        'nav_menu': 'nav_tanaman',
        'tanaman_form': tanaman_form,
        'penjadwalan_form': penjadwalan_form,
    }
    
    if request.method == "GET":
        print("GET")
        if not request.user.is_authenticated:
            return redirect('utama')
        else:
            akun = AKUN.objects.get(user=request.user)
            penjadwalan = PENJADWALAN.objects.filter(akun = akun, tanaman = None)
            context.update({
                'penjadwalan': penjadwalan,
            })
    elif request.method == "POST":
        print("POST")
        if 'tambah' in request.POST:
            akun = AKUN.objects.get(user=request.user)
            
            if tanaman_form.is_valid():
                mode = tanaman_form.cleaned_data.get('mode')
                if mode == 'lembab':
                    min_kelembapan = tanaman_form.cleaned_data.get('min_kelembapan'),
                else:
                    min_kelembapan = 0
                tanaman = TANAMAN.objects.create(
                    pompa = tanaman_form.cleaned_data.get('pompa'),
                    nama_tanaman = tanaman_form.cleaned_data.get('nama_tanaman'),
                    keterangan = tanaman_form.cleaned_data.get('keterangan'),
                    tanggal_menanam = tanaman_form.cleaned_data.get('tanggal_menanam'),
                    min_kelembapan = min_kelembapan,
                    mode=mode,
                    tanggal_aktif = datetime.now(),
                )
                if tanaman.pk:
                    print('berhasil tambah')
                    if mode == 'jadwal':                    
                        update_penjadwalan = PENJADWALAN.objects.filter(akun=akun).update(tanaman=tanaman)
                    request.session['tanaman_tambah_berhasil'] = 'berhasil'
                    return redirect('tanaman:tanaman_tambah_berhasil')
                else:
                    print('gagal tambah')
                penjadwalan = PENJADWALAN.objects.filter(akun=akun)
                context.update({
                    'penjadwalan': penjadwalan,
                    'mode_penyiraman': mode,
                })
            else:
                print('tidak valid')
        elif 'tambah_jadwal' in request.POST:
            akun = AKUN.objects.get(user=request.user)
            
            if penjadwalan_form.is_valid():
                print('valid')
                penjadwalan = PENJADWALAN.objects.create(
                    akun = akun,
                    jam = penjadwalan_form.cleaned_data.get('jam'),
                    menit = penjadwalan_form.cleaned_data.get('menit'),
                    lama_menyiram = penjadwalan_form.cleaned_data.get('lama_menyiram'),
                )
                if penjadwalan.pk:
                    print('berhasil simpan')
                else:
                    print('gagal menyimpan')
            else:
                print('ga valid')
                print(penjadwalan_form.errors)

            penjadwalan = PENJADWALAN.objects.filter(akun=akun)
            context.update({
                'penjadwalan': penjadwalan,
                'mode_penyiraman': 'jadwal',
            })
        # elif 'ubah_jadwal' in request.POST:
        #     print('ubah_jadwal')
        #     akun = AKUN.objects.get(user=request.user)
        #     try:
        #         update_penjadwalan = PENJADWALAN.objects.get(id=int(request.POST['ubah_jadwal']))
        #         if penjadwalan_form.is_valid():
        #             jam = penjadwalan_form.cleaned_data.get('jam')
        #             menit = penjadwalan_form.cleaned_data.get('menit')
        #             lama_menyiram = penjadwalan_form.cleaned_data.get('lama_menyiram')
        #             print(jam)
        #             print(menit)
        #             print(lama_menyiram)
                    
        #             if jam is None:
        #                 print('None')
        #             else:
        #                 print('ada')
                    
        #             # if  jam is None:
        #             #     print('jam')
        #             #     update_penjadwalan.jam = jam
        #             # if not menit is None:
        #             #     print('menit')
        #             #     update_penjadwalan.menit = menit
        #             # if not lama_menyiram is None:
        #             #     print('lama_menyiram')
        #             #     update_penjadwalan.lama_menyiram = lama_menyiram
                        
        #             update_penjadwalan.save()
                    
        #         else:
        #             print('ga valid')
        #     except PENJADWALAN.DoesNotExist:
        #         print('ga ada proses Edit')
                
        #     penjadwalan = PENJADWALAN.objects.filter(akun=akun)
        #     context.update({
        #         'penjadwalan': penjadwalan,
        #         'mode_penyiraman': 'jadwal',
        #     })
        elif 'hapus_jadwal' in request.POST:
            akun = AKUN.objects.get(user=request.user)
            try:
                hapus_penjadwalan = PENJADWALAN.objects.get(id=int(request.POST['hapus_jadwal']))
                hapus_penjadwalan.delete()
            except PENJADWALAN.DoesNotExist:
                print('ga ada proses hapus')
            penjadwalan = PENJADWALAN.objects.filter(akun=akun)
            context.update({
                'penjadwalan': penjadwalan,
                'mode_penyiraman': 'jadwal',
            })
            
    return render(request, 'tanaman/tanaman_tambah.html', context)

def tanaman_ubahView(request):
    if not 'tanaman_ubah_dipilih' in request.session and not request.user.is_authenticated:
        return redirect('utama')    
    tanaman = TANAMAN.objects.get(id=request.session['tanaman_ubah_dipilih'])
    context = {
        'page_title': 'Ubah Tanaman',
        'heading': 'Ubah Tanaman',
        'nav_menu': 'nav_tanaman',
    }
    
    if request.method == "GET":
        print("GET")
        
        data_tanaman = {
            'nama_tanaman': tanaman.nama_tanaman,
            'keterangan' : tanaman.keterangan,
            'min_kelembapan': tanaman.min_kelembapan,
            'tanggal_menanam' : tanaman.tanggal_menanam,
        }
        tanaman_form = tanamanForm(request.user, initial=data_tanaman, instance=tanaman)
        penjadwalan_form = penjadwalanForm()

        context.update({
            'penjadwalan_form': penjadwalan_form,
            'tanaman_form': tanaman_form,
        })
        
        
        if tanaman.mode == 'jadwal':
            penjadwalan = PENJADWALAN.objects.filter(tanaman=tanaman)
            context.update({
                'penjadwalan_form': penjadwalan_form,
                'tanaman_form': tanaman_form,
                'penjadwalan': penjadwalan,
                'mode_penyiraman': tanaman.mode,
            })
        else:
            context.update({
                'penjadwalan_form': penjadwalan_form,
                'tanaman_form': tanaman_form,
                'mode_penyiraman': tanaman.mode,
            })
        
    
    
    elif request.method == "POST":
        print("POST")
        tanaman_form = tanamanForm(request.user, request.POST or None, instance=tanaman)
        penjadwalan_form = penjadwalanForm(request.POST or None)

        context.update({
            'tanaman_form': tanaman_form,
            'penjadwalan_form': penjadwalan_form,
        })
            
        if 'simpan' in request.POST:
            print('post simpan')
            if tanaman_form.is_valid():
                print('berhasil tanaman')
                tanaman_form.save()
                request.session['tanaman_ubah_berhasil'] = 'berhasil'
                return redirect('tanaman:tanaman_ubah_berhasil')  
            else:
                print('tidak valid')
        elif 'tambah_jadwal' in request.POST:
            akun = AKUN.objects.get(user=request.user)
            
            if penjadwalan_form.is_valid():
                print('valid')
                penjadwalan = PENJADWALAN.objects.create(
                    tanaman= tanaman,
                    akun = akun,
                    jam = penjadwalan_form.cleaned_data.get('jam'),
                    menit = penjadwalan_form.cleaned_data.get('menit'),
                    lama_menyiram = penjadwalan_form.cleaned_data.get('lama_menyiram'),
                )
                if penjadwalan.pk:
                    print('berhasil simpan')
                else:
                    print('gagal menyimpan')
            else:
                print('ga valid')
                print(penjadwalan_form.errors)

            penjadwalan = PENJADWALAN.objects.filter(akun=akun)
            context.update({
                'penjadwalan': penjadwalan,
                'mode_penyiraman': 'jadwal',
            })
        elif 'hapus_jadwal' in request.POST:
            akun = AKUN.objects.get(user=request.user)
            try:
                hapus_penjadwalan = PENJADWALAN.objects.get(id=int(request.POST['hapus_jadwal']))
                hapus_penjadwalan.delete()
            except PENJADWALAN.DoesNotExist:
                print('ga ada proses hapus')
            penjadwalan = PENJADWALAN.objects.filter(akun=akun)
            context.update({
                'penjadwalan': penjadwalan,
                'mode_penyiraman': 'jadwal',
            })
        
    return render(request, 'tanaman/tanaman_ubah.html', context)


class berhasilView(View):
    
    template_name = 'tanaman/berhasil.html'
    aksi = None
    context = {}
    
    def get(self, request, *args, **kwargs):
        print('get')
        if not 'tanaman_tambah_berhasil' in request.session and not 'tanaman_ubah_berhasil' in request.session and not 'tanaman_hapus_berhasil' in request.session:
            return redirect('utama')
        else:
            if self.aksi == 'tanaman_tambah_berhasil':
                self.context.update({
                    'page_title': 'Tambah Tanaman Berhasil',
                    'heading': 'Proses Menambahkan Tanaman Berhasil',
                    'body': 'Proses menambahkan Tanaman telah berhasil. Silahkan tekan tombol kembali untuk pergi ke halaman tanaman',
                })
            elif self.aksi == 'tanaman_ubah_berhasil':
               self.context.update({
                    'page_title': 'Update tanaman Berhasil',
                    'heading': 'Proses Menyimpan Perubahan Tanaman Anda Berhasil',
                    'body': 'Proses menyimpan perubahan pada tanaman anda berhasil disimpan. Silahkan tekan tombol kembali untuk pergi ke halaman tanaman',
                }) 
            elif self.aksi == 'tanaman_hapus_berhasil':
               self.context.update({
                    'page_title': 'Update Tanaman Berhasil',
                    'heading': 'Proses Menyimpan Perubahan Tanaman Anda Berhasil',
                    'body': 'Proses menghapus data tanaman anda berhasil. Silahkan tekan tombol kembali untuk pergi ke halaman tanaman',
                }) 
        return render(request, self.template_name, self.context)