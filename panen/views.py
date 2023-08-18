from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import PREDIKSI_PANEN, HASIL_PANEN
from .forms import panenForm, hasil_panenForm, prediksi_panenForm
from tanaman.models import TANAMAN, JENIS_TANAMAN
from datetime import date, timedelta
import math

# Create your views here.

def knn(training,suhu,jumlah_air,kelembapan,k):
    # mencari nilai banyaknya data training 
    length = len(training)
    
    print("## Menghitung Jarak")
    print("------------------------------------------------------------------------------------------")
    # Menghitung jarak
    for i in range(length):
        jarak = round(math.sqrt((training[i]["suhu"] - suhu)**2 + (training[i]["jumlah_air"] - jumlah_air)**2 + (training[i]["kelembapan"] - kelembapan)**2),4)
        
        training[i].update({"Jarak" : jarak})
        print(i+1,".",training[i])
    
    print("")
    print("## Mengurutkan Jarak Secara Ascending")
    print("------------------------------------------------------------------------------------------")
    # Mengurutkan data training secara ascending berdasarkan nilai jaraknya
    training = sorted(training, key=lambda x:x["Jarak"], reverse=False)
    
    for i in range(length):
        print(i+1,".",training[i]) 
    print("")

    BERHASIL_PANEN = 0
    GAGAL_PANEN = 0
    print("## Data yang termasuk sebagai tetangga terdekat sebanyak nilai K(",k,")")
    print("------------------------------------------------------------------------------------------")
    # Menghitung banyaknya nilai klasifikasi YA dan TIDAK pada data yang termasuk sebagai tetangga terdekat
    for i in range(k):
        print(i+1,".",training[i])
        if training[i]["status_panen"] == True:
            BERHASIL_PANEN += 1
        elif training[i]["status_panen"] == False:
            GAGAL_PANEN += 1

    print("")
    print("## Pilih Mayoritas")
    print("------------------------------------------------------------------------------------------")
    print("BERHASIL_PANEN = ", BERHASIL_PANEN)
    print("GAGAL_PANEN = ", GAGAL_PANEN)
    
    # Membandingkan jumlah klasifikasi YA dan TIDAK
    klasifikasi = "null"
    if BERHASIL_PANEN > GAGAL_PANEN:
        klasifikasi = True
    elif BERHASIL_PANEN < GAGAL_PANEN:
        klasifikasi = False
    print("Mayoritas = ", klasifikasi)

    return klasifikasi

def normalisasi(training,suhu,jumlah_air, kelembapan):
    # Menambah data uji untuk diikut sertakan dalam proses normalisasi
    training.append({"suhu":suhu, "jumlah_air":jumlah_air, 'kelembapan': kelembapan})
    
    # mencari nilai(nilainya masih 1 row data) terbesar dan terkecil dari atribut suhu dan jumlah_air
    maks_suhu = max(training, key=lambda x:x["suhu"])
    mins_suhu = min(training, key=lambda x:x["suhu"])
    maks_jumlah_air = max(training, key=lambda x:x["jumlah_air"])
    mins_jumlah_air = min(training, key=lambda x:x["jumlah_air"])
    maks_kelembapan = max(training, key=lambda x:x["kelembapan"])
    mins_kelembapan = min(training, key=lambda x:x["kelembapan"])
    
    # mencari nilai(angkanya) terbesar dan terkecil dari atribut suhu dan jumlah_air
    maks_suhu = maks_suhu["suhu"]
    mins_suhu = mins_suhu["suhu"]
    maks_jumlah_air = maks_jumlah_air["jumlah_air"]
    mins_jumlah_air = mins_jumlah_air["jumlah_air"]
    maks_kelembapan = maks_kelembapan["kelembapan"]
    mins_kelembapan = mins_kelembapan["kelembapan"]

    norm_suhu = 0 
    norm_jumlah_air = 0
    norm_kelembapan = 0
    length = len(training)

    # melakukan perhitungan normalisasi min-max
    for i in range(length):
        if i == length-1:
            norm_suhu = training[i]["suhu"] = round((training[i]["suhu"] - mins_suhu) / (maks_suhu - mins_suhu),4)
            norm_jumlah_air = training[i]["jumlah_air"] = round((training[i]["jumlah_air"] - mins_jumlah_air) / (maks_jumlah_air - mins_jumlah_air),4)
            norm_kelembapan = training[i]["kelembapan"] = round((training[i]["kelembapan"] - mins_kelembapan) / (maks_kelembapan - mins_kelembapan),4)
            
        else:
            training[i]["suhu"] = round((training[i]["suhu"] - mins_suhu) / (maks_suhu - mins_suhu),4)
            training[i]["jumlah_air"] = round((training[i]["jumlah_air"] - mins_jumlah_air) / (maks_jumlah_air - mins_jumlah_air),4)
            training[i]["kelembapan"] = round((training[i]["kelembapan"] - mins_kelembapan) / (maks_kelembapan - mins_kelembapan),4)
            

    # membuang nilai data uji yang sebelumnya di ikut sertakan untuk di normalisasikan
    training.pop()
    
    return norm_suhu, norm_jumlah_air, norm_kelembapan

@csrf_exempt
def test_panenView(request):
    panen_form = panenForm(request.POST or None)
    K = 7
    context = {
        'page_title': 'Panen',
        'heading': 'Test Keberhasilan Panen',
        'nav_menu': 'nav_test_panen',
        'panen_form': panen_form,
    }
    if request.method == "GET":
        print('get')
        if not request.user.is_authenticated:
            return redirect('/login/')
    elif request.method == "POST":
        if 'prediksi' in request.POST:
            print('prediksi')
            if panen_form.is_valid():
                print('valid')
                suhu = panen_form.cleaned_data.get('suhu')
                jumlah_air = panen_form.cleaned_data.get('jumlah_air')
                kelembapan = panen_form.cleaned_data.get('kelembapan')
                panen = PREDIKSI_PANEN.objects.all()
                data_training = []
                
                for data in panen:
                    row = {}
                    row['suhu'] = data.suhu
                    row['jumlah_air'] = data.jumlah_air
                    row['kelembapan'] = data.kelembapan
                    row['status_panen'] = data.status_panen
                    data_training.append(row)
                print(suhu)
                print(jumlah_air)
                print(kelembapan)
                print(data_training)        
                norm_suhu, norm_jumlah_air, norm_kelembapan = normalisasi(data_training,suhu,jumlah_air,kelembapan)
                # Memanggil fungsi knn dan mengembalikan nilai berupa hasil dari klasifikasinya
                output_klasifikasi = knn(data_training,norm_suhu,norm_jumlah_air,norm_kelembapan,K)

                print("")
                print("## Output")
                print("------------------------------------------------------------------------------------------")
                print("HASIL KLASIFIKASI PANEN =", output_klasifikasi)
                if output_klasifikasi:
                    request.session['klasifikasi_panen_berhasil'] = 'berhasil'
                    return redirect('panen:klasifikasi_berhasil')
                else:
                    request.session['klasifikasi_panen_gagal'] = 'berhasil'
                    return redirect('panen:klasifikasi_gagal')
            else:
                print('ga valid')
    
    return render(request, 'panen/panen.html', context)

@csrf_exempt
def hasil_panen_listView(request): 
    context = {
        'page_title': 'Panen',
        'heading': 'Hasil Panen',
        'nav_menu': 'nav_hasil_panen',
    }
    if request.method == "GET":
        print('get')
        if not request.user.is_authenticated:
            return redirect('/login/')
        else:
            hasil_panen = HASIL_PANEN.objects.filter(tanaman__akun__user=request.user)
            context.update({
                'hasil_panen': hasil_panen,
            })
    elif request.method == "POST":
        if 'ubah' in request.POST:
            request.session['hasil_panen_ubah_dipilih'] = int(request.POST.get('ubah'))
            return redirect('panen:hasil_panen_ubah')
        elif 'hapus' in request.POST:
            print('hapus')
            hasil_panen = HASIL_PANEN.objects.get(id=int(request.POST.get('hapus')))
            hasil_panen.delete()
            request.session['hasil_panen_hapus_berhasil'] = 'berhasil'
            return redirect('panen:hasil_panen_hapus_berhasil')
        
    return render(request, 'panen/hasil_panen_list.html', context)

@csrf_exempt
def hasil_panen_tambahView(request):
    
    hasil_panen_form = hasil_panenForm(request.user, request.POST or None)
    context = {
        'page_title': 'Tambah Panen',
        'heading': 'Prediksi Panen',
        'nav_menu': 'nav_hasil_panen',
        'hasil_panen_form': hasil_panen_form,
    }
    
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect('utama')
    elif request.method == "POST":
        if 'tambah' in request.POST:
            if hasil_panen_form.is_valid():
                
                hasil_panen = HASIL_PANEN.objects.create(
                    tanaman = hasil_panen_form.cleaned_data.get('tanaman'),
                    jumlah_buah = hasil_panen_form.cleaned_data.get('jumlah_buah'),
                    tanggal_panen = hasil_panen_form.cleaned_data.get('tanggal_panen'),
                
                )
                if hasil_panen.pk:
                    print('berhasil tambah')
                    request.session['hasil_panen_tambah_berhasil'] = 'berhasil'
                    return redirect('panen:hasil_panen_tambah_berhasil')
                else:
                    print('gagal tambah')
    return render(request, 'panen/hasil_panen_tambah.html', context)
  
def hasil_panen_ubahView(request):
    if not 'hasil_panen_ubah_dipilih' in request.session and not request.user.is_authenticated:
        return redirect('utama')    
    hasil_panen = HASIL_PANEN.objects.get(id=request.session['hasil_panen_ubah_dipilih'])
    context = {
        'page_title': 'Panen',
        'heading': 'Prediksi Panen',
        'nav_menu': 'nav_hasil_panen',
    }
    
    if request.method == "GET":
        print("GET")
        hasil_panen_form = hasil_panenForm(request.user, instance=hasil_panen)

        context.update({
            'hasil_panen_form': hasil_panen_form,
        })
        
    elif request.method == "POST":
        print("POST")
        hasil_panen_form = hasil_panenForm(request.user, request.POST or None, instance=hasil_panen)

        context.update({
            'hasil_panen_form': hasil_panen_form,
        })
            
        if 'simpan' in request.POST:
            print('post simpan')
            if hasil_panen_form.is_valid():
                print('berhasil tanaman')
                hasil_panen_form.save()
                request.session['hasil_panen_ubah_berhasil'] = 'berhasil'
                return redirect('panen:hasil_panen_ubah_berhasil')  
            else:
                print('tidak valid')
        
    return render(request, 'panen/hasil_panen_ubah.html', context)
   
@csrf_exempt
def prediksi_panenView(request):
    prediksi_panen_form = prediksi_panenForm(request.user, request.POST or None)

    context = {
    'page_title': 'Prediksi Panen Selanjutnya',
    'heading': 'Prediksi Panen',
    'nav_menu': 'nav_prediksi_panen',
    'prediksi_panen_form': prediksi_panen_form,
    }
    if request.method == "GET":
        print('get')
        if not request.user.is_authenticated:
            return redirect('/login/')
        
    elif request.method == "POST":
        if 'tanaman' in request.POST:
            if prediksi_panen_form.is_valid():
                try:    
                    hasil_panen = HASIL_PANEN.objects.filter(tanaman=prediksi_panen_form.cleaned_data.get('tanaman')).latest('id')
                    lama_panen = hasil_panen.tanaman.jenis_tanaman.waktu_panen
                    tanggal_panen = hasil_panen.tanggal_panen + timedelta(days=lama_panen)

                    context.update({
                        'terakhir_panen': hasil_panen.tanggal_panen,
                        'tanggal_panen' : tanggal_panen,
                    })
                    print('ada')
                except HASIL_PANEN.DoesNotExist:
                    print('ga ada')
                    tanaman = TANAMAN.objects.get(id=prediksi_panen_form.cleaned_data.get('tanaman').id)
                    context.update({
                        'pertama_menanam': tanaman.tanggal_menanam,
                    })
    return render(request, 'panen/prediksi_panen.html', context)
   
class klasifikasiView(View):
    
    template_name = 'panen/klasifikasi.html'
    aksi = None
    context = {}
    
    def get(self, request, *args, **kwargs):
        print('get')
        if not 'klasifikasi_panen_berhasil' in request.session and not 'klasifikasi_panen_gagal' in request.session:
            return redirect('utama')
        else:
            if self.aksi == 'klasifikasi_panen_berhasil':
                self.context.update({
                    'page_title': 'Klasifikasi Berhasil Panen',
                    'heading': 'Tumbuhan Anda Akan Panen',
                    'body': 'Selamat, tumbuhan anda akan panen. Silahkan menekan tombol kembali untuk pergi ke halaman panen',
                    'klasifikasi': 'berhasil',
                })
            elif self.aksi == 'klasifikasi_panen_gagal':
                self.context.update({
                    'page_title': 'Klasifikasi Gagal Panen',
                    'heading': 'Tumbuhan Anda Akan Gagal Panen',
                    'body': 'Sayang Sekali, tumbuhan anda akan mengalami gagal panen. Silahkan menekan tombol kembali untuk pergi ke halaman panen',
                    'klasifikasi': 'gagal',
                })
        return render(request, self.template_name, self.context)
    
    
class berhasilView(View):
    
    template_name = 'panen/berhasil.html'
    aksi = None
    context = {}
    
    def get(self, request, *args, **kwargs):
        print('get')
        if not 'hasil_panen_tambah_berhasil' in request.session and not 'hasil_panen_ubah_berhasil' in request.session and not 'hasil_panen_hapus_berhasil' in request.session:
            return redirect('utama')
        else:
            if self.aksi == 'hasil_panen_tambah_berhasil':
                self.context.update({
                    'page_title': 'Tambah Hasil Panen Berhasil',
                    'heading': 'Proses Menambahkan Hasil Panen Berhasil',
                    'body': 'Proses menambahkan hasil panen telah berhasil. Silahkan tekan tombol kembali untuk pergi ke halaman hasil panen',
                })
            elif self.aksi == 'hasil_panen_ubah_berhasil':
               self.context.update({
                    'page_title': 'Update hasil panen Berhasil',
                    'heading': 'Proses Menyimpan Perubahan hasil panen Anda Berhasil',
                    'body': 'Proses menyimpan perubahan pada hasil panen anda berhasil disimpan. Silahkan tekan tombol kembali untuk pergi ke halaman hasil panen',
                }) 
            elif self.aksi == 'hasil_panen_hapus_berhasil':
               self.context.update({
                    'page_title': 'Update Tanaman Berhasil',
                    'heading': 'Proses Menyimpan Perubahan Hasil Panen Anda Berhasil',
                    'body': 'Proses menghapus data hasil panen anda berhasil. Silahkan tekan tombol kembali untuk pergi ke halaman hasil panen',
                }) 
        return render(request, self.template_name, self.context)