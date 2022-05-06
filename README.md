# 가상환경 설정
1. 프로젝트 수행 첫번째 단계로 가상환경을 만든다.
- 가상환경은 프로젝트 마다 별도로 생성하는 것이 타당하다. 아무튼 먼저 필요한 패키지 설치
``````````````````
$ python -m pip install virtualenv
``````````````````
- 설치한 패키지를 이용하여 가상환경 생성
``````````````````
$ virtualenv evsp-venv
$ source evsp-venv/scripts/activate
``````````````````
- 가상환경이 활성화되면 django 설치
``````````````````
$ pip install django
``````````````````
2. 장고 프로젝트 생성
- 먼저 django-admin을 이용하여 프로젝트 생성 및 앱 생성
- 프로젝트명 evsp_comm
- 프로젝트 내 앱 이름 board, evuser, evcharger
``````````````````
$ django-admin startproject evsp_comm
$ cd evsp_comm
$ django-admin startapp board
$ django-admin startapp evuser
``````````````````
3. 앱 만들기
- 앱 폴더 내부에 templates 폴더를 만든다. 앱들은 templates 폴더 내의 화일들을 찾게된다.
- 앱 폴더 내의 models.py를 작성한다.
``````````````````
from django.db import models

# Create your models here.

class Evuser(models.Model):
  username = models.CharField(max_length=64, verbose_name='사용자명')
  password = models.CharField(max_length=64, verbose_name='비밀번호')
  register_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')

  class Meta:
    db_table = 'evsp_evuser'
``````````````````
- 앱이 만들어지면 프로젝트 폴더의 settings.py 화일에 생성된 앱을 등록해 준다.
``````````````````
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'board',
    'evuser',
]
``````````````````

4. 앱 모델에 따라서 데이터베이스 생성
```````````````````
$ python manage.py makemigrations
$ python manage.py migrate
```````````````````
- 명령의 수행을 마치면 프로젝트 화일 내에 db.sqlite3 라는 DB가 생성된다.
- sqlite3로 DB 생성이 제대로 되었는지 확인 가능함

5. 앱을 구동하여 사용해 보기
- DB 생성이 되고 나면 앱을 구동한다. 앱을 구동하기에 앞서 본 프로젝트를 관리하는 수퍼유저를 등록한다.
``````````````````
$ python manage.py createsuperuser
Username (leave blank to use 'jeongsooh'): 
Email address: jeongsooh@hotmail.com
Password: 
Password (again): 
Superuser created successfully.
``````````````````
- 수퍼유저 ID/password는 다음으로 설정 jeongsooh / evsp#1234
- 수퍼유저를 등록하고 나면 아래와 같이 서버를 구동한다.
``````````````````
$ python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
May 03, 2022 - 01:15:05
Django version 4.0.4, using settings 'evsp_comm.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
``````````````````
- 상기 주소를 통해서 서버에 접속할 수 있다.

6. 작성한 앱들을 admin 사이트에 등록 및 사용하기 위하여 각 앱의 구성화일 중에서 admin.py를 작성한다.
``````````````````
from django.contrib import admin
from .models import Evuser

# Register your models here.

class EvuserAdmin(admin.ModelAdmin):
  list_display = ('username', 'password', 'register_dttm')

admin.site.register(Evuser, EvuserAdmin)
``````````````````
7. 작성한 앱들의 상세 기능을 구현하기 위하여 templates 폴더에 html 화일들을 작성한다.
- html 화일은 bootstrap을 사용할 것이므로 cdn 관련 화일을 바로 링크해서 사용(https://getbootstrap.com/)
- 사용자 등록을 위하여 register.html 화일 작성
8. 작성된 html 화일을 프로젝트와 연결하기 위하여 views.py 화일을 작성한다.
- 작성된 views.py 샘플
``````````````````
from django.shortcuts import render

# Create your views here.
def register(request):
  return render(request, 'register.html')
``````````````````
- views.py 화일이 작성되면 프로젝트 폴더의 urls.py를 업데이트 한다.
``````````````````
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('evuser/', include('evuser.urls')),
]
``````````````````
- 그런데, evuser.urls 화일이 없으므로 evuser 앱 폴더에 urls.py 화일을 작성해 준다.
``````````````````
from django.urls import path
from . import views

# path()는 경로와 관련된 함수를 가지고 call 한다.
# 따라서 함수를 정의한 views.py를 import 해야 하고, views에서 정의한 함수를 경로와 맺어준다.

urlpatterns = [
    path('register/', views.register),
]
``````````````````
- 브라우저를 통해서 ~/evuser/register.html 실행하여 연결이 완성되었는지 확인한다.

9. 회원가입 페이지를 통하여 입력된 회원가입 내용이 실제로 데이터베이스에 기록되고 연동될 수 있는 비즈니스 로직을 작성한다.
- 먼저 html 화일에서 필요한 내용을 입력 샘플의 일부를 보면 아래와 같다. form 테그에 POST 또는 GET 등 적시, action="" name="" 정의하고 특히 {% csrf_token %} 꼭 form 안에 입력한다.
``````````````````
        <form method="POST" action=".">
          <!-- django에서 폼에서 서버로 데이터를 전송할 때 보안을 위해서 꼭 넣어줘야 하는 기능  -->
          <!-- 비즈니스 로직을 작성하고 POST를 통해 데이터 전달을 위해서는 name="" 이 꼭 있어야 해서 추가. -->
          {% csrf_token %} 
          <div class="mb-3">
            <label for="username" class="form-label">사용자 이름</label>
            <input type="text" class="form-control" id="username" placeholder="사용자 이름" name="username">
          </div> 
`````````````````` 
- 다음은 views.py에서 전달받은 데이터를 처리하는 기능을 작성한다.
`````````````````````
# Create your views here.
def register(request):
  if request.method == 'GET':
    return render(request, 'register.html')
  elif request.method == 'POST':
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    re_password = request.POST.get('re-password', None)

    res_data = {}
    if not (username and password and re_password):
      res_data['error'] = '모든 값을 입력해야 합니다.'
    elif password != re_password:
      res_data['error'] = '비밀번호가 다릅니다.'
    else:
      evuser = Evuser(
        username=username,
        password=make_password(password)
      )
      evuser.save()

    return render(request, 'register.html', res_data) 
``````````````````````````````

10. 회원가입 페이지가 완성되고 나면 회원에 관한 필드를 추가한다.
- 예를 들면 이메일 필드를 추가한다.
- 이 메일 필드를 추가하면 Models이 변경되므로 다시 makemigrations 와 migrate를 실행해서 DB를 재구성 해야 한다. 
- 이 때 기존의 data에는 새로이 추가된 필드의 값을 어떻게 할 것인지 선택하고 수행한다. 예를 들면 아래와 같다.
```````````````````````````
$ python manage.py makemigrations
It is impossible to add a non-nullable field 'email' to evuser without specifying a default. This is because the database needs something to populate existing rows.
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit and manually define a default value in models.py.
Select an option: 1
Please enter the default value as valid Python.
The datetime and django.utils.timezone modules are available, so it is possible to provide e.g. timezone.now as a value.
Type 'exit' to exit this prompt
>>> 'test@gmail.com'
Migrations for 'evuser':
  evuser\migrations\0002_alter_evuser_options_evuser_email.py
    - Change Meta options on evuser
    - Add field email to evuser
(evsp-venv)
jeongsooh@DESKTOP-ISVFPRU MINGW64 ~/Documents/projects/python/django/EVSP/evsp_comm (master)
$
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, evuser, sessions
Running migrations:
  Applying evuser.0002_alter_evuser_options_evuser_email... OK
(evsp-venv) 
jeongsooh@DESKTOP-ISVFPRU MINGW64 ~/Documents/projects/python/django/EVSP/evsp_comm (master)
$ 
```````````````````````````
11. CSS, JS 화일 추가하는 방법
- CSSm JS 화일을 추가하려면 프로젝트 폴더에 static 이란 폴더를 만든 후 static 폴더에 넣어두면 된다.
- static 폴더는 프로젝트 폴더의 settings.py에 아래와 같이 등록해야 한다. 
`````````````````````````````
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
`````````````````````````````
- Bootstrap thema를 하나 다운로드 받아서 적용한 샘플은 다음과 같다.
- bootstrap thema free 중에서 하나의 테마를 지원하는 샘플을  download 받은 후 static 폴더에 복사한다. bootstrap cdn link를 disable 시키고 대신 static에 download 받은 화일을 활성화 시킨다.
-----------------------------
  <!-- CSS only -->
  <!-- <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous"> -->
  <link rel="stylesheet" href="/static/bootstrap.min.css" />
-----------------------------

12. 다음은 세션을 관리하는 로그인 화면을 만든다.
- 먼저 login.html/logout.html 화일을 만든다.
```````````````````````
def logout(request):
  if request.session.get('user'):
    del(request.session['user'])
  
  return redirect('/')

def login(request):
  if request.method == 'GET':
    return render(request, 'login.html')
  elif request.method == 'POST':
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)

    res_data = {}
    if not (username and password):
      res_data['error'] = '모든 값을 입력해야 합니다.'
    else:
      evuser = Evuser.objects.get(username=username)
      print(evuser)
      if check_password(password, evuser.password):
        request.session['user'] = evuser.id
        return redirect('/')
      else:
        res_data['error'] = '비밀번호가 틀렸습니다.'
    return render(request, 'login.html')
`````````````````````````````````````````
13. templates file들이 중복 작성되는 것을 방지하기 위한 상속 처리하기
- 기본이 되는 html 화일에서 특정 단위의 특정 공간 배정
`````````````````````````````````````````
<html>
<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- CSS only -->
  <link rel="stylesheet" href="/static/bootstrap.min.css" />
</head>
<body>
  <div class="container">
    {% block contents %} 
    {% endblock %} 
  </div>
  
</body>
</html>
`````````````````````````````````````````
- 상속을 받고자 하는 file들은 아래와 같이 작성
`````````````````````````````````````````
{% extends "base.html" %}

{% block contents %}
<div class="row mt-5">
  <div class="col-12">
    {{ error }}
  </div>
</div>
<div class="row mt-5">
  <div class="col-12">
    <form method="POST" action=".">
      {% csrf_token %} 
      <div class="mb-3">
        <label for="username" class="form-label">사용자 이름</label>
        <input type="text" class="form-control" id="username" placeholder="사용자 이름" name="username">
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">비밀번호</label>
        <input type="password" class="form-control" id="password" placeholder="비밀번호" name="password">
      </div>
      <button type="submit" class="btn btn-primary">로그인</button>
    </form>
  </div>
</div>
{% endblock %}
`````````````````````````````````````````

14. 다음은 django에서 제공하는 forms 사용법 익히기. 먼저 login.html을 수정해 본다.
- 먼저 forms.py 화일을 만든다. forms를 이용해서 form을 하나 만든다.
`````````````````````````````````````````
from django import forms

class LoginForm(forms.Form):
  username = forms.CharField(max_length=32)
  password = forms.CharField()
`````````````````````````````````````````
- views.py에서 LoginForm을 login.html로 전달한다.
`````````````````````````````````````````
def login(request):
  form = LoginForm()

  return render(request, 'login.html', {'form': form})
`````````````````````````````````````````
- login.html에서 전달된 데이터를 출력한다.
`````````````````````````````````````````
<form method="POST" action=".">
  {% csrf_token %} 
    {{ form }}
  <button type="submit" class="btn btn-primary">로그인</button>
</form>
`````````````````````````````````````````
- 일단 form 데이터가 login.html로 전달이 된 것은 확인했으므로 form을 통해서 전달된 데이터를 하나씩 그리는 작업을 수행한다.
`````````````````````````````````````````
<form method="POST" action=".">
  {% csrf_token %} 
  {% for field in form %} 
  <div class="form-group mb-3">
    <label for="{{ field.id_for_label }}" class="">{{ field.label }}</label>
    <input type="{{ field.field.widget.input_type }}" class="form-control" 
      id="{{ field.id_for_label }}" placeholder="{{ field.label }}" name="{{ field.name }}" />
  </div>
  {% endfor %}
  <button type="submit" class="btn btn-primary">로그인</button>
</form>
`````````````````````````````````````````
- form은 유사하게 만들어졌으나 실제 field명을 한글로 보여주고 패스워드는 보이지 않아야 하는 등 손질이 필요하다. 이 부분은 forms.py에서 추가적으로 아래와 같은 작업을 수행한다.
`````````````````````````````````````````
from django import forms

class LoginForm(forms.Form):
  username = forms.CharField(max_length=32, label="사용자 이름")
  password = forms.CharField(widget=forms.PasswordInput, label="비밀번호")
`````````````````````````````````````````
- 이제 form은 완성이 되었으므로 실제 login에 필요한 business logic과 연결시키는 작업을 수행한다.
- 먼저 views.py로 전달된 form이 유효한지를 검사한다. 유효하지 않을 경우 field 값에 errors 메세지가 전달되므로 이를 login.html엣 출력하도록 한다.
`````````````````````````````````````````
def login(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      return redirect('/')
  else:
    form = LoginForm()

  return render(request, 'login.html', {'form': form})
`````````````````````````````````````````
`````````````````````````````````````````
<form method="POST" action=".">
  {% csrf_token %} 
  {% for field in form %} 
  <div class="form-group mb-3">
    <label for="{{ field.id_for_label }}" class="">{{ field.label }}</label>
    <input type="{{ field.field.widget.input_type }}" class="form-control" 
      id="{{ field.id_for_label }}" placeholder="{{ field.label }}" name="{{ field.name }}" />
  </div>
  {% if field.errors %}
  <span style="color:red;">{{ field.errors }}</span>
  {% endif %}
  {% endfor %}
  <button type="submit" class="btn btn-primary">로그인</button>
</form>
`````````````````````````````````````````
- 다음은 form에 전달된 field 값이 있는지 여부에 더해서 실제 데이터가 맞는지, 사용자명과 패스워드가 유효한지를 확인한다. 이 부분은 forms.py에서 clean 함수로 확인하도록 한다.
`````````````````````````````````````````
class LoginForm(forms.Form):
  username = forms.CharField(max_length=32, label="사용자 이름")
  password = forms.CharField(widget=forms.PasswordInput, label="비밀번호")
  
  def clean(self):
    cleaned_data = super().clean()
    username = cleaned_data.get('username')
    password = cleaned_data.get('password')

    if username and password:
      evuser = Evuser.objects.get(username=username)
      if not check_password(password, evuser.password):
        self.add_error('password', '비밀번호가 틀렸습니다.')
`````````````````````````````````````````
- 추가적으로 각 field에 문제가 있을 때 영문으로 메세지가 나오는 것을 한글로 바꾸는 작업이 필요한데, 이부분은 forms.py에서 form을 만들 때 해당 필드에 error 메세지를 아래와 같이 넣어주면 된다.
`````````````````````````````````````````
  username = forms.CharField(
    error_messages={
      'required': '사용자명을 입력해 주세요.'
    }, 
    max_length=32, label="사용자 이름")
  password = forms.CharField(
    error_messages={
      'required': '비밀번호를 입력해 주세요.'
    }, 
    widget=forms.PasswordInput, label="비밀번호")
`````````````````````````````````````````
- 마지막으로 세션관리를 추가한다. 먼저 데이터의 유효성을 검증한 forms에서 비밀번호까지 확인하고 난 후 해당 사용자의 id를 session 정보에 넣어 준다.
`````````````````````````````````````````
    if username and password:
      evuser = Evuser.objects.get(username=username)
      if not check_password(password, evuser.password):
        self.add_error('password', '비밀번호가 틀렸습니다.')
      else:
        self.user_id = evuser.id
`````````````````````````````````````````
- 그 다음 session 정보에 들어있는 사용자 id를 views.py에서 login.html로 전달
`````````````````````````````````````````
def login(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      request.session['user'] = form.user_id
      return redirect('/')
  else:
    form = LoginForm()

  return render(request, 'login.html', {'form': form})
`````````````````````````````````````````

15. 게시판 만들기
- 모델 만들기
````````````````````````
from django.db import models
from evuser.models import Evuser

# Create your models here.

class Board(models.Model):
  title = models.CharField(max_length=128, verbose_name='제목')
  contents = models.TextField(verbose_name='내용')
  writer = models.ForeignKey('evuser.Evuser', on_delete=models.CASCADE, verbose_name='작성자')
  register_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')

  def __str__(self):
    return self.title

  class Meta:
    db_table = 'evsp_board'
    verbose_name = '게시글'
    verbose_name_plural = '게시글'
````````````````````````
- views.py 작성
````````````````````````
from django.shortcuts import render
from .models import Board

# Create your views here.

def board_list(request):
  boards = Board.objects.all().order_by('-id')
  return render(request, 'board_list.html', {'boards': boards})
````````````````````````
- board_list.html 작성
````````````````````````
<table class="table table-light">
      <thead class="thead-light">
        <tr>
          <th>#</th>
          <th>제목</th>
          <th>아이디</th>
          <th>일시</th>
        </tr>
      </thead>
      <tbody class="text-dark">
        {% for board in boards %}
        <tr>
          <th>{{ board.id }}</th>
          <td>{{ board.title }}</td>
          <td>{{ board.writer }}</td>
          <td>{{ board.register_dttm }}</td>        
        </tr>
        {% endfor %}
      </tbody>
    </table>
````````````````````````
- BoardAdmin  작성 및 admin 사이트 등록
````````````````````````
from django.contrib import admin
from .models import Board

# Register your models here.

class BoardAdmin(admin.ModelAdmin):
  list_display = ('title', )

admin.site.register(Board, BoardAdmin)
````````````````````````
- 프로젝트 urls.py에 등록
````````````````````````
urlpatterns = [
    path('admin/', admin.site.urls),
    path('evuser/', include('evuser.urls')),
    path('board/', include('board.urls')),
    path('', home)
]
````````````````````````
- board 앱 urls.py 도 생성
````````````````````````
from django.urls import path
from . import views

# path()는 경로와 관련된 함수를 가지고 call 한다.
# 따라서 함수를 정의한 views.py를 import 해야 하고, views에서 정의한 함수를 경로와 맺어준다.

urlpatterns = [
    path('list/', views.board_list),
]
````````````````````````
- 다음은 board_write.html (게시판 글쓰기)를 만들기 위해서 BoardForm을 forms.py로 작성(????? 왜????)
````````````````````````
from django import forms

class BoardForm(forms.Form):
  title = forms.CharField(
    error_messages={
      'required': '제목을 입력해 주세요.'
    }, 
    max_length=128, label="제목")
  contents = forms.CharField(
    error_messages={
      'required': '내용을 입력해 주세요.'
    }, 
    widget=forms.Textarea, label="내용")
````````````````````````
- 작성된 forms에 관련한 views, url 작성
````````````````````````
from django.shortcuts import render
from .models import 
from .forms import BoardForm

# Create your views here.
def board_write(request):
  form = BoardForm()
  return render(request, 'board_write.html', { 'form': form })

def board_list(request):
  boards = Board.objects.all().order_by('-id')
  return render(request, 'board_list.html', {'boards': boards})
````````````````````````
````````````````````````
urlpatterns = [
    path('list/', views.board_list),
    path('write/', views.board_write),
]
````````````````````````
- board_write.html 작성
````````````````````````
      {% for field in form %} 
      <div class="form-group mb-3">
        <label for="{{ field.id_for_label }}" class="">{{ field.label }}</label>
        {% if field.name == 'contents' %}
        <textarea class="form-control" name="{{ field.name }}" placeholder="{{ field.label }}"></textarea>
        {% else %}
        <input type="{{ field.field.widget.input_type }}" class="form-control" 
          id="{{ field.id_for_label }}" placeholder="{{ field.label }}" name="{{ field.name }}" />
        {% endif %}
      </div>
      {% if field.errors %}
````````````````````````
- 게시물 작성자를 자동으로 삽입할 수 있는 기능을 views.py에서 구현한다.
````````````````````````
def board_write(request):
  if request.method == 'POST':
    form = BoardForm(request.POST)
    if form.is_valid():
      user_id = request.session.get('user')
      evuser = Evuser.objects.get(pk=user_id)

      board = Board()
      board.title = form.cleaned_data['title']
      board.contents = form.cleaned_data['contents']
      board.writer = evuser
      board.save()

      return redirect('/board/list')

  else:
    form = BoardForm()
  return render(request, 'board_write.html', { 'form': form })
````````````````````````
- 다음은 게시물 상세 보기를 작성한다. 먼저 views.py에서 board_detail 함수 작성
````````````````````````
def board_detail(request, pk):
  board = Board.objects.get(pk=pk)
  return render(request, 'board_detail.html', {'board': board})
````````````````````````
- pk 값을 활용할 수 있도록 urls.py 화일 수정
````````````````````````
urlpatterns = [
    path('detail/<int:pk>/', views.board_detail),
    path('list/', views.board_list),
    path('write/', views.board_write),
]
````````````````````````
- board_detail.html 화일을 작성한다.
````````````````````````
<div class="row mt-5">
  <div class="col-12">
    <div class="form-group mb-3">
      <label for="title" class="">제목</label>
      <input type="text" class="form-control" id="title" value="{{ board.title }}" readonly/>
      <label for="contents" class="">내용</label>
      <textarea class="form-control" readonly>{{ board.contents }}</textarea>
    </div>
    <button class="btn btn-primary">돌아가기</button>
  </div>
</div>
````````````````````````

16. 예외처리 
- 먼저 등록되어있지 않은 사용자일 경우 유효성 검사하는 clean()에서 예외처리한다.
````````````````````````
      try:
        evuser = Evuser.objects.get(username=username)
      except Evuser.DoesNotExist:
        self.add_error('username', '아이디가 없습니다.')
        return
````````````````````````
- 다음은 게시판에서 글이 없을 때...
````````````````````````
def board_detail(request, pk):
  try:
    board = Board.objects.get(pk=pk)
  except Board.DoesNotExist:
    raise Http404('게시글을 찾을 수 없습니다.')

  return render(request, 'board_detail.html', {'board': board})
````````````````````````
- 게시판에 글을 올리려고 할 때, 사용자가 로그인을 하지 않은 상태라면 게시자를 등록할 수 없으므로.. board_write 초기에 세션을 체크해서 사용자가 로그인한 상태인지 체크하는 루틴 삽입
````````````````````````
def board_write(request):
  if not request.session.get('user'):
    return redirect('/evuser/login/')
````````````````````````
17. 다음은 게시판 page 관리 - 일정 갯수로 페이지를 구성하고 페이지 간 네비게이션 지원
- 먼저 html 화일에서 기본 구조를 그린다.
````````````````````````
<div class="row mt-2">
  <div class="col-12">
    <nav>
      <ul class="pagination justify-content-center">
        <li class="page-item">
          <a href="#" class="page-link">이전으로</a>
        </li>
        <li class="page-item active">
          <a href="#" class="page-link">1 / 1</a>
        </li>
        <li class="page-item">
          <a href="#" class="page-link">다음으로</a>
        </li>
      </ul>
    </nav>
  </div>
</div>
````````````````````````
- django에서  제공하는 paginator란 기능을 이용하여 views.py에서 페이지를 제어하는 함수를 작성한다.
````````````````````````
def board_list(request):
  all_boards = Board.objects.all().order_by('-id')
  page = int(request.GET.get('p', 1))
  paginator = Paginator(all_boards, 2)
  boards = paginator.get_page(page)
  return render(request, 'board_list.html', {'boards': boards})
````````````````````````
- views.py에서 구성한 pagination 정보가 이미 boards에 들어가 있으므로 상기 게시판 관리페이지에 적용해서 html 화일을 업데이트 한다.
````````````````````````
    <nav>
      <ul class="pagination justify-content-center">
        {% if boards.has_previous %}
        <li class="page-item">
          <a href="?p={{ boards.previous_page_number }}" class="page-link">이전으로</a>
        </li>
        {% else %}
        <li class="page-item disabled">
          <a href="#" class="page-link">이전으로</a>          
        </li>
        {% endif %}
        <li class="page-item active">
          <a href="#" class="page-link">{{ boards.number }} / {{ boards.paginator.num_pages }}</a>
        </li>
        {% if boards.has_next %}
        <li class="page-item">
          <a href="?p={{ boards.next_page_number }}" class="page-link">다음으로</a>
        </li>
        {% else %}
        <li class="page-item disabled">
          <a href="#" class="page-link">다음으로</a>          
        </li>
        {% endif %}
      </ul>
    </nav>
````````````````````````
18. 홈 페이지부터 기능들을 조직화하는 작업, 링크들 엮어서 사이트처럼 보이게..
- 먼저 home.html을 작성한다.
````````````````````````
{% block contents %}
<div class="row mt-5">
  <div class="col-12 text-center">
    <h1>홈페이지입니다.</h1>
  </div>
</div>
<div class="row mt-5">
  <div class="col-6 d-grid gap-2">
    <button class="btn btn-primary" onclick="location.href='/evuser/login/'">로그인</button>
  </div>
  <div class="col-6 d-grid gap-2">
    <button class="btn btn-primary" onclick="location.href='/evuser/register/'">회원가입</button>
  </div>
</div>
<div class="row mt-1">
  <div class="col-12 d-grid gap-2">
    <button class="btn btn-primary" onclick="location.href='/board/list/'">게시물보기</button>
  </div>
</div>
{% endblock %}
````````````````````````
- 다음은 views.py에서 만들어 놓은 home 함수에서 rendering 할 수 있도록 수정한다.
````````````````````````
def home(request):
  user_id = request.session.get('user')
  if user_id:
    evuser = Evuser.objects.get(pk=user_id)

  return render(request, 'home.html')
````````````````````````
- 사용자의 로그인 여부에 따라서 홈페이지에서 보여주는 내용이 바뀌어야 하므로 views.home에서 수행하는 session 관련 기능을 home.html 화일에서 직접하도록 수정한다. 아래와 같이 변경한다.
````````````````````````
def home(request):
  return render(request, 'home.html')
````````````````````````
````````````````````````
  {% if request.session.user %}  
  <div class="col-12 d-grid gap-2">
    <button class="btn btn-primary" onclick="location.href='/evuser/logout/'">로그아웃</button>
  </div>
  {% else %}
  <div class="col-6 d-grid gap-2">
    <button class="btn btn-primary" onclick="location.href='/evuser/login/'">로그인</button>
  </div>
  <div class="col-6 d-grid gap-2">
    <button class="btn btn-primary" onclick="location.href='/evuser/register/'">회원가입</button>
  </div>
  {% endif %}
````````````````````````
- 기타 필요한 링크는 onclick="location.href='/board/list'" 활용해서 구성. 예로 리스트에서 상세 읽기를 하고자 할 경우 아래와 같이 board_list.html에서 tr tag에 onclick을 설정한다. 아래와 같다.
````````````````````````
        <tr onclick="location.href='/board/detail/{{ board.id }}'">
          <th>{{ board.id }}</th>
          <td>{{ board.title }}</td>
          <td>{{ board.writer }}</td>
          <td>{{ board.register_dttm }}</td>        
        </tr>
````````````````````````

19. 게시판에 테그를 활용할 수 있도록 tag 앱도 만들고 활용하기 위한 작성을 한다.
- 먼저 아래와 같은 명령을 실행해서 테그앱을 작성한다.
````````````````````````
$ python manage.py startapp tag
````````````````````````
- 새로운 폴더가 생기고 그 안에 models, views, admin 모두 작성한다. 먼저 models.py
````````````````````````
from django.db import models

# Create your models here.

class Tag(models.Model):
  name = models.CharField(max_length=32, verbose_name='테그명')
  register_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')

  def __str__(self):
    return self.name

  class Meta:
    db_table = 'evsp_tag'
    verbose_name = '테그'
    verbose_name_plural = '테그'
````````````````````````
- 다음은 admin.py
````````````````````````
from django.contrib import admin
from .models import Tag

# Register your models here.

class TagAdmin(admin.ModelAdmin):
  list_display = ('name', )

admin.site.register(Tag, TagAdmin)
````````````````````````
- 이제 board.Board에 tag 기능을 추가한다. 아래와 같이 board.Board 모델에 등록한다.
````````````````````````
from django.db import models
from evuser.models import Evuser
from tag.models import Tag

# Create your models here.

class Board(models.Model):
  title = models.CharField(max_length=128, verbose_name='제목')
  contents = models.TextField(verbose_name='내용')
  writer = models.ForeignKey('evuser.Evuser', on_delete=models.CASCADE, verbose_name='작성자')

  tags = models.ManyToManyField('tag.Tag', verbose_name='테그')

  register_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')

  def __str__(self):
    return self.title

  class Meta:
    db_table = 'evsp_board'
    verbose_name = '게시글'
    verbose_name_plural = '게시글'
````````````````````````
- 다음은 프로젝트 settings.py에 tag 앱을 등록해 준다.
````````````````````````
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'board',
    'evuser',
    'tag',
]
````````````````````````
- 앱 등록을 마치면 아래와 같은 명령을 통해서 DB 생성 및 migration
````````````````````````
$ python manage.py makemigrations
Migrations for 'tag':
  tag\migrations\0001_initial.py     
    - Create model Tag
Migrations for 'board':
  board\migrations\0002_board_tags.py
    - Add field tags to board
(evsp-venv) 
jeongsooh@DESKTOP-ISVFPRU MINGW64 ~/Documents/projects/python/django/EVSP/evsp_comm (master)
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, board, contenttypes, evuser, sessions, tag
Running migrations:
  Applying tag.0001_initial... OK
  Applying board.0002_board_tags... OK
(evsp-venv) 
jeongsooh@DESKTOP-ISVFPRU MINGW64 ~/Documents/projects/python/django/EVSP/evsp_comm (master)
$
````````````````````````
- 다음은 글쓰기에서 실제로 테그를 생성. 먼저 forms.py에서 테그 폼 생성
````````````````````````
tags = forms.CharField(required=False, label="테그")
````````````````````````
- 글쓰기에서 넘어온 테그를 받아서 입력하는 작업을 views.py에서 작성한다.
````````````````````````
    if form.is_valid():
      user_id = request.session.get('user')
      evuser = Evuser.objects.get(pk=user_id)

      tags = form.cleaned_data['tags'].split(',')

      board = Board()
      board.title = form.cleaned_data['title']
      board.contents = form.cleaned_data['contents']
      board.writer = evuser
      board.save()

      for tag in tags:
        if not tag:
          cotinue
        _tag, _ = Tag.objects.get_or_create(name=tag)
        board.tags.add(_tag)
        
      return redirect('/board/list')
````````````````````````
- board_detail.py에서 tag를 포함 출력할 수 있도록 작성
````````````````````````
    <div class="form-group mb-3">
      <label for="title" class="">제목</label>
      <input type="text" class="form-control" id="title" value="{{ board.title }}" readonly/>
      <label for="contents" class="">내용</label>
      <textarea class="form-control" readonly>{{ board.contents }}</textarea>
      <label for="tags" class="">테그</label>
      <span id="tags" class="form-control">
        {{ board.tags.all | join:", "}}
      </span>
    </div>
    <button class="btn btn-primary" onclick="location.href='/board/list/'">돌아가기</button>
````````````````````````
20. 이제 작성된 프로젝트를 배포하는 방법
- 먼저 settings.py 내에서 DEBUG 모드를 off 시킨다. 그리고 본 프로젝트를 올릴 서버를 지정해 준다. pythonanywhere 서비스를 사용할 경우 사용자 계정명의 서버 이름(아래의 예시). 모든 서버로 할 경우 '*' 도 사용가능.
````````````````````````
DEBUG = False
ALLOWED_HOSTS = [
  'jeongsooh.pythonanywhere.com'
]
````````````````````````
- static 화일들을 정리해서 한곳에 모아둘 것이므로 아래와 같이 새로운 static 화일 경로를 지정해 준다.
````````````````````````
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
````````````````````````
- 다음은 소스파일을 압축해서 배포용 서버로 올린다. evsp_comm 프로젝트 폴더만 압축한다. evsp-venv 폴더는 가상환경을 제공하는 화일들로 실제 배포용 서버에서 새롭게 환경을 설정해야 한다.
- pythonanywhere의 예
- unzip으로 압축을 푼다. 그리고 가상환경을 설치한다. 가상환경 설치 시 python version도 지정해 준다. 설치가 완료되면 가상환경을 활성화 시킨다. 그 다음 django를 설치한다.
````````````````````````
03:48 ~ $ unzip *.zip
Archive:  evsp_comm.zip
   creating: evsp_comm/board/
 extracting: evsp_comm/board/__init__.py  
   creating: evsp_comm/board/__pycache__/
  inflating: evsp_comm/board/__pycache__/__init__.cpython-310.pyc  

03:48 ~ $
03:48 ~ $ 
03:51 ~ $ virtualenv --python=python3.7 evsp-env
created virtual environment CPython3.7.10.final.0-64 in 9200ms
  creator CPython3Posix(dest=/home/jeongsooh/evsp-env, clear=False, no_vcs_ignore=False, global=False)
  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=/home/jeongsooh/.local/share/virtualenv)
    added seed packages: pip==22.0.4, setuptools==62.0.0, wheel==0.37.1
  activators BashActivator,CShellActivator,FishActivator,PowerShellActivator,PythonActivator,XonshActivator
03:52 ~ $ 
03:52 ~ $ 
03:54 ~ $ source evsp-env/bin/activate
(evsp-env) 03:54 ~ $ 
(evsp-env) 03:54 ~ $ pip install django
Installing collected packages: pytz, typing-extensions, sqlparse, asgiref, django
Successfully installed asgiref-3.5.1 django-3.2.13 pytz-2022.1 sqlparse-0.4.2 typing-extensions-4.2.0
(evsp-env) 04:29 ~ $ 
(evsp-env) 03:54 ~ $ 
``````````````````````````````````````````````````````````
- 이제 패키지 설치는 완료되었고, 프로젝트 안으로 들어가서 필요한 명령을 실행한다. 제일 먼저 static 화일들을 수집하고 migration을 실행한다. DB를 가져간 경우 특별히 많은 작업을 수행하지는 않는다. 모든 것이 완료되면 exit를 실행해서 bash 화면에서 빠져나간다. 그리고 브라우져의 뒤로 화살표를 눌러서 pythonanywhere 첫 화면으로 넘어간다.
``````````````````````````````````````````````````````````
(evsp-env) 03:54 ~ $ cd evsp
(evsp-env) 04:31 ~ $ cd evsp_comm
(evsp-env) 04:31 ~/evsp_comm $ ls
board  db.sqlite3  evcharger  evsp_comm  evuser  manage.py  static  tag
(evsp-env) 04:31 ~/evsp_comm $ 
(evsp-env) 04:31 ~/evsp_comm $ python manage.py collectstatic
You have requested to collect static files at the destination
location as specified in your settings:
    /home/jeongsooh/evsp_comm/static
This will overwrite existing files!
Are you sure you want to do this?
Type 'yes' to continue, or 'no' to cancel: yes
128 static files copied to '/home/jeongsooh/evsp_comm/static'.
(evsp-env) 04:33 ~/evsp_comm $ 
(evsp-env) 04:35 ~/evsp_comm $ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, board, contenttypes, evuser, sessions, tag
Running migrations:
  No migrations to apply.
(evsp-env) 04:35 ~/evsp_comm $ 
(evsp-env) 04:35 ~/evsp_comm $ 
(evsp-env) 04:35 ~/evsp_comm $ 
(evsp-env) 04:35 ~/evsp_comm $ exit
exit
Console closed.
``````````````````````````````````````````````````````````
- 다음은 pythonanywhere에서 필요한 설정을 수행한다. Web 메뉴선택 > Add a new web app 선택 > Next 선택 > Phthon Web Framework 메뉴에선 하단의 Manual configuration 선택 > Python version은 3.7 선택 후 Next 선택
- 기본 설정 마친 후 Configuration for jeongsooh pythonanywhere 화면이 나옴
- 여기서 Code 항목에서 source code 경로 설정 (예, /home/jeongsooh/evsp_comm)
- WSGI 설정을 위해 해당 링크를 누르면 편집을 할 수 있는데, 기존의 내용을 모두 주석처리하고 다음과 같이 입력하고 우측 상단의 저장 버튼을 누른 후 다시 뒤로 가기 화살표를 눌러서 구성 화면으로 복귀한다.
``````````````````````````````````````````````````````````
# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys

# assuming your django settings file is at '/home/jeongsooh/mysite/mysite/settings.py'
# and your manage.py is is at '/home/jeongsooh/mysite/manage.py'
path = '/home/jeongsooh/evsp_comm'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'evsp_comm.settings'

# then:
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
``````````````````````````````````````````````````````````
- 다음은 구성 메뉴에서 Virtualenv: 항목에서 경로를 설정해 준다. (예, /home/jeongsooh/evsp-env)
- 다음은 Static files: 항목에서 화일들을 연결해 준다. URL 밑에 '/static/'을 등록하고 경로는 '/home/jeongsooh/evsp_comm/static/'을 등록해 준다.
- 그 다음 제일 위 쪽에 위치한 Reload 버튼을 선택해서 다시 시작한다. 











