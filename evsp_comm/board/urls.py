from django.urls import path
from . import views

# path()는 경로와 관련된 함수를 가지고 call 한다.
# 따라서 함수를 정의한 views.py를 import 해야 하고, views에서 정의한 함수를 경로와 맺어준다.

urlpatterns = [
    path('detail/<int:pk>/', views.board_detail),
    path('list/', views.board_list),
    path('write/', views.board_write),
]