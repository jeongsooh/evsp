# Generated by Django 4.0.4 on 2022-05-12 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Evcharger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpname', models.CharField(max_length=64, verbose_name='충전기이름')),
                ('cpnumber', models.CharField(max_length=64, verbose_name='충전기번호')),
                ('cpstatus', models.CharField(max_length=64, verbose_name='충전상태')),
                ('address', models.TextField(verbose_name='주소')),
                ('cpversion', models.CharField(max_length=64, verbose_name='펌웨어버전')),
                ('register_dttm', models.DateTimeField(auto_now_add=True, verbose_name='등록일시')),
            ],
            options={
                'verbose_name': '충전기',
                'verbose_name_plural': '충전기',
                'db_table': 'evsp_evcharger',
            },
        ),
    ]