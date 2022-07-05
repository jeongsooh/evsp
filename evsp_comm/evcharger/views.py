from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Evcharger
from evuser.models import Evuser
from .forms import EvchargerForm

# Create your views here.

def evcharger_list(request):
  all_evchargers = Evcharger.objects.all().order_by('-id')
  page = int(request.GET.get('p', 1))
  paginator = Paginator(all_evchargers, 2)
  evchargers = paginator.get_page(page)

  user_id = request.session.get('user')
  if user_id:
    loginuser = Evuser.objects.get(pk=user_id)

  return render(request, 'evcharger_list.html', {'loginuser': loginuser, 'evchargers': evchargers})

def evcharger_detail(request, pk):
  try:
    evcharger = Evcharger.objects.get(pk=pk)
  except Evcharger.DoesNotExist:
    raise Http404('충전기 상세내역을 찾을 수 없습니다.')

  return render(request, 'evcharger_detail.html', {'evcharger': evcharger})

def evcharger_write(request):
  if not request.session.get('user'):
    return redirect('/evuser/login/')

  if request.method == 'POST':
    form = EvchargerForm(request.POST)
    if form.is_valid():
      # user_id = request.session.get('user')
      # evuser = Evuser.objects.get(pk=user_id)

      # tags = form.cleaned_data['tags'].split(',')

      evcharger = Evcharger()
      evcharger.cpname = form.cleaned_data['cpname']
      evcharger.cpnumber = form.cleaned_data['cpnumber']
      evcharger.cpstatus = form.cleaned_data['cpstatus']
      evcharger.address = form.cleaned_data['address']
      evcharger.cpversion = form.cleaned_data['cpversion']
      # cardinfo.writer = evuser
      evcharger.save()

      # for tag in tags:
      #   if not tag:
      #     cotinue
      #   _tag, _ = Tag.objects.get_or_create(name=tag)
      #   board.tags.add(_tag)

      return redirect('/evcharger/list')

  else:
    form = EvchargerForm()
  return render(request, 'evcharger_write.html', { 'form': form })
