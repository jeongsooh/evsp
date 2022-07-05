from django import forms
from .models import Evcharger
from django.contrib.auth.hashers import check_password

class EvchargerForm(forms.Form):
  cpname = forms.CharField(
    error_messages={
      'required': '충전기이름을 입력해 주세요.'
    }, 
    max_length=32, label="충전기이름")
  cpnumber = forms.CharField(
    error_messages={
      'required': '충전기번호를 입력해 주세요.'
    }, 
    max_length=32, label="충전기번호")
  cpstatus = forms.CharField(max_length=32, label="충전상태")
  # address = forms.TextField(label="주소")
  cpversion = forms.CharField(max_length=32, label="펌웨어버전")
  register_dttm = forms.DateTimeField(label='등록일시')
  # def clean(self):
  #   cleaned_data = super().clean()
  #   username = cleaned_data.get('username')
  #   password = cleaned_data.get('password')

  #   if username and password:
  #     try:
  #       evuser = Evuser.objects.get(username=username)
  #     except Evuser.DoesNotExist:
  #       self.add_error('username', '아이디가 없습니다.')
  #       return
  #     if not check_password(password, evuser.password):
  #       self.add_error('password', '비밀번호가 틀렸습니다.')
  #     else:
  #       self.user_id = evuser.id