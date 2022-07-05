from django import forms
from .models import Cardinfo
from django.contrib.auth.hashers import check_password

class CardinfoForm(forms.Form):
  cardname = forms.CharField(
    error_messages={
      'required': '카드이름을 입력해 주세요.'
    }, 
    max_length=32, label="카드이름")
  cardtag = forms.CharField(
    error_messages={
      'required': '카드테그를 입력해 주세요.'
    }, 
    max_length=32, label="카드테그")
  cardstatus = forms.CharField(max_length=32, label="카드상태")
  ownername = forms.CharField(max_length=32, label="회원번호")
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