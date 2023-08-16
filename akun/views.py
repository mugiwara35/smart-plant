from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import AKUN
from .forms import loginForm, userForm, akunForm, update_userForm


# Create your views here.
@csrf_exempt
def loginView(request):
    login_form = loginForm(request.POST or None)
    context = {
        'page_title': 'Login',
        'login_form': login_form,
    }
    if request.method == "GET":
        print('get')
        if request.user.is_authenticated:
            return redirect('utama')
        else:
            if 'register_berhasil' in request.session:
                del request.session['register_berhasil']
            print('belum login')
    elif request.method == "POST":
        if 'login' in request.POST:
            if login_form.is_valid():
                print('valid')
                user = authenticate(request, username=login_form.cleaned_data.get('username'), password=login_form.cleaned_data.get('password'))
                if user is not None:
                    print('login')
                    login(request,user)
                    return redirect('utama')
                else:
                    print('gagal_login')
                    context.update({
                        'error_login': "Gagal Login, username atau password yang anda masukkan salah",
                    })
            else:
                print('ga valid')
        print('post')
    return render(request, 'akun/login.html', context)

@csrf_exempt
def registerView(request):
    user_form = userForm(request.POST or None)
    akun_form = akunForm(request.POST or None)
    context = {
        'page_title': 'Register',
        'user_form': user_form,
        'akun_form': akun_form,
    }
    if request.method == "GET":
        print('get')
        if request.user.is_authenticated:
            return redirect('utama')
        else:
            print('belum punya akun')
    elif request.method == "POST":
        if 'register' in request.POST:
            if user_form.is_valid() and akun_form.is_valid():
                print('valid')
                if user_form.cleaned_data.get('password') == user_form.cleaned_data.get('password_validasi'):
                    print('password sama')
                    akun = AKUN.objects.filter(user__username=user_form.cleaned_data.get('username'))
                    if len(akun) > 0:
                        print('username sudah ada')
                        context.update({
                            'username_error': 'Username sudah terdaftar. Harap mengganti usernamenya!'
                        })
                    else:
                        print('username belum ada')
                        proses_user = User.objects.create_user(
                            username=user_form.cleaned_data.get('username'),
                            password=user_form.cleaned_data.get('password'),
                        )
                        proses_user.save()
                        if proses_user.pk:
                            print('berhasil bikin user')
                            proses_akun = AKUN.objects.create(
                                user=proses_user,
                                nama=akun_form.cleaned_data.get('nama'),
                            )
                            if proses_akun.pk:
                                print('berhasil bikin akun')
                                request.session['register_berhasil'] = 'berhasil'
                                return redirect('akun:register_berhasil')
                else:
                    print('password beda')
                    context.update({
                        'password_error': 'Password tidak sesuai. Harap mengisi password dengan benar!'
                    })
            else:
                print('tidak valid')
        print('post')
    
    return render(request, 'akun/register.html', context)

@csrf_exempt
def update_akunView(request):
    user = User.objects.get(id=request.user.id)
    akun = AKUN.objects.get(user=request.user)
    context = {
        'page_title': 'Akun Anda',
        'nav_menu': 'nav_akun',
    }
    if request.method == "GET":
        print('get')
        if not request.user.is_authenticated:
            return redirect('utama')
        else:
            print('sudah login')
            
            data_user = {
                'username': request.user.username,
            }
            data_akun = {
                'nama': akun.nama,
            }
            update_user_form = update_userForm(initial=data_user, instance=user)
            akun_form = akunForm(initial=data_akun, instance=akun)
            context.update({
                'update_user_form': update_user_form,
                'akun_form': akun_form,
            })
    elif request.method == "POST":
        print('post')
        update_user_form = update_userForm(request.POST or None, instance=user)
        akun_form = akunForm(request.POST or None, instance=akun)
        context.update({
            'update_user_form': update_user_form,
            'akun_form': akun_form,
        })
        if 'simpan' in request.POST:
            print('simpan')
            if update_user_form.is_valid() and akun_form.is_valid():
                print('valid')
                update_user_form.save()
                akun_form.save()
                request.session['update_akun_berhasil'] = 'berhasil'
                return redirect('akun:update_akun_berhasil')
            else:
                print(update_user_form.errors)
                print(akun_form.errors)
                print('ga valid')
    return render(request,'akun/akun.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutView(request):
    logout(request)
    return redirect('utama')

class berhasilView(View):
    template_name = 'akun/berhasil.html'
    aksi = None
    context = {}
    
    def get(self, request, *args, **kwargs):
        print('get')
        if not 'register_berhasil' in request.session and not 'update_akun_berhasil' in request.session:
            return redirect('utama')
        else:
            if self.aksi == 'register_berhasil':
                self.context.update({
                    'page_title': 'Register Berhasil',
                    'heading': 'Proses Register Berhasil',
                    'body': 'Proses register telah berhasil. Silahkan tekan tombol kembali untuk pergi ke halaman login',
                    'kembali': 'register',
                })
            elif self.aksi == 'update_akun_berhasil':
               self.context.update({
                    'page_title': 'Update Akun Berhasil',
                    'heading': 'Proses Menyimpan Perubahan Akun Anda Berhasil',
                    'body': 'Proses menyimpan perubahan pada akun anda berhasil disimpan. Silahkan tekan tombol kembali untuk pergi ke halaman akun anda',
                    'kembali': 'update_akun',
                }) 
        return render(request, self.template_name, self.context)