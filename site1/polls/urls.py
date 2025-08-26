from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.index, name='base'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('preview/', views.preview_view, name='preview'),
    path('arena-web-hooking/', views.arena_receiver, name='arena-web-hooking'),
    path('arena-web-hooking-show/', views.arena_show, name='arena-web-hooking-show'),
    path('pbi-repo/', views.pbi_view, name='pbi-repo'),
    path('chaveamento/<int:id_evento>/', views.chaveamento_view, name='chaveamento'),
    path('lutas-json/', views.lutas_json)
    ]
