from django import forms
from .models import Charginginfo
from django.contrib.auth.hashers import check_password

class CharginginfoForm(forms.Form):
  cpname = forms.CharField(
    error_messages={
      'required': '충전기이름을 입력해 주세요.'
    }, 
    max_length=32, label="충전기이름")
  chargedname = forms.CharField(
    error_messages={
      'required': '사용자명을 입력해 주세요.'
    }, 
    max_length=32, label="사용자명")
    # widget=forms.PasswordInput, label="사용자명")
  energy = forms.IntegerField(label="충전량")
  amount = forms.IntegerField(label="충전금액")
  start_dttm = forms.DateTimeField(label='충전시작일시')
  end_dttm = forms.DateTimeField(label='충전완료일시')
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