from participants import views
from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.send_participants),
    path('csv/', views.get_participants),
    path('delete/', views.delete_database),
    path('ladder_all/', views.ladder_all),
    path('ladder_tournament/', views.ladder_tournament),
    path('buildladder_all/', views.buildladder_all),
]