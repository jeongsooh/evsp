from django.urls import path
from . import views

# path()는 경로와 관련된 함수를 가지고 call 한다.
# 따라서 함수를 정의한 views.py를 import 해야 하고, views에서 정의한 함수를 경로와 맺어준다.

urlpatterns = [
    path('detail/<int:pk>/', views.evuser_detail),
    path('list/', views.evuser_list),
    # path('write/', views.evuser_write),
    path('evuser_register/', views.evuser_register),
    path('login/', views.login),
    path('logout/', views.logout),
]