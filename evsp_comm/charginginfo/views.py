from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Charginginfo
from evuser.models import Evuser
from .forms import CharginginfoForm

# Create your views here.

def charginginfo_list(request):
  all_charginginfos = Charginginfo.objects.all().order_by('-id')
  page = int(request.GET.get('p', 1))
  paginator = Paginator(all_charginginfos, 2)
  charginginfos = paginator.get_page(page)

  user_id = request.session.get('user')
  if user_id:
    loginuser = Evuser.objects.get(pk=user_id)

  return render(request, 'charginginfo_list.html', {'loginuser': loginuser, 'charginginfos': charginginfos})

def charginginfo_detail(request, pk):
  try:
    charginginfo = Charginginfo.objects.get(pk=pk)
  except Charginginfo.DoesNotExist:
    raise Http404('충전정보 상세내역을 찾을 수 없습니다.')

  return render(request, 'charginginfo_detail.html', {'charginginfo': charginginfo})

def charginginfo_write(request):
  if not request.session.get('user'):
    return redirect('/evuser/login/')

  if request.method == 'POST':
    form = CharginginfoForm(request.POST)
    if form.is_valid():
      # user_id = request.session.get('user')
      # evuser = Evuser.objects.get(pk=user_id)

      # tags = form.cleaned_data['tags'].split(',')

      charginginfo = Charginginfo()
      charginginfo.cpname = form.cleaned_data['cpname']
      charginginfo.chargedname = form.cleaned_data['chargedname']
      # charginginfo.writer = evuser
      charginginfo.save()

      # for tag in tags:
      #   if not tag:
      #     cotinue
      #   _tag, _ = Tag.objects.get_or_create(name=tag)
      #   board.tags.add(_tag)

      return redirect('/charginginfo/list')

  else:
    form = CharginginfoForm()
  return render(request, 'charginginfo_write.html', { 'form': form })