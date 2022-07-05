from django.db import models

# Create your models here.

class Evuser(models.Model):
  USER_STATUS = [
    ('CONTRACTED', '정상'),
    ('NOT_CONTRACTED', '해지'),
    ('STOPED', '유예'),
  ]
  USER_CATEGORY = [
    ('NORMAL', '일반'),
    ('GROUPED', '법인'),
    ('ETC', '기타'),
  ]

  username = models.CharField(max_length=64, verbose_name='사용자명')
  password = models.CharField(max_length=128, verbose_name='비밀번호')
  usernumber = models.CharField(max_length=64, verbose_name='회원번호')
  name = models.CharField(max_length=64, verbose_name='회원이름')
  email = models.EmailField(max_length=128, verbose_name='이메일')
  phone = models.CharField(max_length=64, verbose_name='전화번호')
  category = models.CharField(max_length=64, 
    choices=USER_CATEGORY, default='NORMAL', verbose_name='회원구분')
  status = models.CharField(max_length=64, 
    choices=USER_STATUS, default='CONTRACTED', verbose_name='회원상태')
  address = models.TextField(verbose_name='주소')
  register_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')

  def __str__(self):
    return self.username

  class Meta:
    db_table = 'evsp_evuser'
    verbose_name = '사용자'
    verbose_name_plural = '사용자'

