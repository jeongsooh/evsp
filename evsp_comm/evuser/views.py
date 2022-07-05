from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password, check_password
from .models import Evuser
from .forms import LoginForm

# Create your views here.
def home(request):
  return render(request, 'home.html')

def svchome(request):
  user_id = request.session.get('user')
  if user_id:
    loginuser = Evuser.objects.get(pk=user_id)

  all_evusers = Evuser.objects.all().order_by('-id')
  page = int(request.GET.get('p', 1))
  paginator = Paginator(all_evusers, 5)
  evusers = paginator.get_page(page)

  return render(request, 'svchome.html', {'loginuser': loginuser, 'evusers': evusers})

def logout(request):
  if request.session.get('user'):
    del(request.session['user'])
  
  return redirect('/')

def login(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      request.session['user'] = form.user_id
      return redirect('/evuser/list')
      # return redirect('/svchome')
  else:
    form = LoginForm()

  return render(request, 'login.html', {'form': form})

def evuser_register(request):
  if request.method == 'GET':
    return render(request, 'register.html')
  elif request.method == 'POST':
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    re_password = request.POST.get('re-password', None)
    name = request.POST.get('name', None)
    email = request.POST.get('email', None)
    phone = request.POST.get('phone', None)
    address = request.POST.get('address', None)

    res_data = {}
    if not (username and email and phone and password and re_password):
      res_data['error'] = '모든 값을 입력해야 합니다.'
    elif password != re_password:
      res_data['error'] = '비밀번호가 다릅니다.'
    else:
      evuser = Evuser(
        username=username,
        password=make_password(password),
        name=name,
        email=email,
        phone=phone,
        address=address
      )
      evuser.save()

    return render(request, 'register.html', res_data) 

def evuser_detail(request, pk):
  try:
    evuser = Evuser.objects.get(pk=pk)
  except Evuser.DoesNotExist:
    raise Http404('사용자를 찾을 수 없습니다.')

  return render(request, 'evuser_detail.html', {'evuser': evuser})

def evuser_list(request):
  user_id = request.session.get('user')
  if user_id:
    loginuser = Evuser.objects.get(pk=user_id)

  all_evusers = Evuser.objects.all().order_by('-id')
  page = int(request.GET.get('p', 1))
  paginator = Paginator(all_evusers, 2)
  evusers = paginator.get_page(page)

  return render(request, 'evuser_list.html', {'loginuser': loginuser, 'evusers': evusers})