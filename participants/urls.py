from participants import views
from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.send_participants),
    path('csv/', views.get_participants),
    path('delete/', views.delete_database),
    path('ladder1/', views.ladder),
    path('ladder2/', views.ladder2),
]