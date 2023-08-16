from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import PANEN
from .forms import panenForm
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
def panenView(request):
    panen_form = panenForm(request.POST or None)
    K = 7
    context = {
        'page_title': 'Panen',
        'heading': 'Prediksi Panen',
        'nav_menu': 'nav_panen',
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
                panen = PANEN.objects.all()
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