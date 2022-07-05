from django.db import models

# Create your models here.

class Evcharger(models.Model):
  cpname = models.CharField(max_length=64, verbose_name='충전기이름')
  cpnumber = models.CharField(max_length=64, verbose_name='충전기번호')
  cpstatus = models.CharField(max_length=64, verbose_name='충전상태')
  address = models.TextField(verbose_name='주소')
  cpversion = models.CharField(max_length=64, verbose_name='펌웨어버전')
  register_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록일시')

  def __str__(self):
    return self.cpname

  class Meta:
    db_table = 'evsp_evcharger'
    verbose_name = '충전기'
    verbose_name_plural = '충전기'