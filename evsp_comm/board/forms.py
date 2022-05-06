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
  tags = forms.CharField(required=False, label="테그")

  # def clean(self):
  #   cleaned_data = super().clean()
  #   username = cleaned_data.get('username')
  #   password = cleaned_data.get('password')

  #   if username and password:
  #     evuser = Evuser.objects.get(username=username)
  #     if not check_password(password, evuser.password):
  #       self.add_error('password', '비밀번호가 틀렸습니다.')
  #     else:
  #       self.user_id = evuser.id
