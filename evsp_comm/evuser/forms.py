from django import forms
from .models import Evuser
from django.contrib.auth.hashers import check_password

class LoginForm(forms.Form):
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

  def clean(self):
    cleaned_data = super().clean()
    username = cleaned_data.get('username')
    password = cleaned_data.get('password')

    if username and password:
      try:
        evuser = Evuser.objects.get(username=username)
      except Evuser.DoesNotExist:
        self.add_error('username', '아이디가 없습니다.')
        return
      if not check_password(password, evuser.password):
        self.add_error('password', '비밀번호가 틀렸습니다.')
      else:
        self.user_id = evuser.id
