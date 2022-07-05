from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Cardinfo
from evuser.models import Evuser
from .forms import CardinfoForm

# Create your views here.

def cardinfo_list(request):
  all_cardinfos = Cardinfo.objects.all().order_by('-id')
  page = int(request.GET.get('p', 1))
  paginator = Paginator(all_cardinfos, 2)
  cardinfos = paginator.get_page(page)

  user_id = request.session.get('user')
  if user_id:
    loginuser = Evuser.objects.get(pk=user_id)

  return render(request, 'cardinfo_list.html', {'loginuser': loginuser, 'cardinfos': cardinfos})

def cardinfo_detail(request, pk):
  try:
    cardinfo = Cardinfo.objects.get(pk=pk)
  except Cardinfo.DoesNotExist:
    raise Http404('충전카드 상세내역을 찾을 수 없습니다.')

  return render(request, 'cardinfo_detail.html', {'cardinfo': cardinfo})

def cardinfo_write(request):
  if not request.session.get('user'):
    return redirect('/evuser/login/')

  if request.method == 'POST':
    form = CardinfoForm(request.POST)
    if form.is_valid():
      # user_id = request.session.get('user')
      # evuser = Evuser.objects.get(pk=user_id)

      # tags = form.cleaned_data['tags'].split(',')

      cardinfo = Cardinfo()
      cardinfo.cpname = form.cleaned_data['cpname']
      cardinfo.chargedname = form.cleaned_data['chargedname']
      # cardinfo.writer = evuser
      cardinfo.save()

      # for tag in tags:
      #   if not tag:
      #     cotinue
      #   _tag, _ = Tag.objects.get_or_create(name=tag)
      #   board.tags.add(_tag)

      return redirect('/cardinfo/list')

  else:
    form = CardinfoForm()
  return render(request, 'cardinfo_write.html', { 'form': form })