from django.urls import path

from . import views

app_name = 'lmygame'
urlpatterns = [
    path('', views.index, name='index'),
    path('/login', views.login, name='login'),
    path('/selection', views.selection, name='selection'),
    path('/name_plate_list', views.name_plate_list, name='name_plate_list'),
    path('/question', views.question, name='question'),
    path('/result', views.result, name='result'),
]
