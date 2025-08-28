from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.index, name='base'),
    path('preview/', views.preview_view, name='preview'),
    path('arena-web-hooking/', views.arena_receiver, name='arena-web-hooking'),
    path('arena-web-hooking-show/', views.arena_show, name='arena-web-hooking-show'),
    path('pbi-repo/', views.pbi_view, name='pbi-repo'),
    path('lutas-json/', views.lutas_json),
    path("credentials/", views.credentials_list, name="credentials_list"),
    path("credentials/new/", views.credentials_create, name="credentials_create"),
    path("credentials/<int:pk>/edit/", views.credentials_edit, name="credentials_edit"),
    path("credentials/<int:pk>/delete/", views.credentials_delete, name="credentials_delete"),
    path('eventos-sge/', views.eventos_sge_list, name='eventos_sge_list'),
    path('eventos-arena-load/', views.eventos_sge_upload, name='eventos_sge_upload')
    ]
