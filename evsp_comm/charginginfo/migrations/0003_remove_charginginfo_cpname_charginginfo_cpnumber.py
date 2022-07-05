# Generated by Django 4.0.4 on 2022-05-12 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evcharger', '0001_initial'),
        ('charginginfo', '0002_remove_charginginfo_cpnumber_charginginfo_cpname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='charginginfo',
            name='cpname',
        ),
        migrations.AddField(
            model_name='charginginfo',
            name='cpnumber',
            field=models.ForeignKey(default=100, on_delete=django.db.models.deletion.CASCADE, to='evcharger.evcharger', verbose_name='충전기번호'),
            preserve_default=False,
        ),
    ]
