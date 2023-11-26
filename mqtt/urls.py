from django.urls import path
from . import views

app_name = 'mqtt'
urlpatterns = [
    path('<int:quantity>/', views.home, name='home'),
    path('htc/', views.htc_ajax.as_view(), name='htc'),
    path('h/', views.htc_merge.as_view(), name='htc_merge'),
    path('', views.home, name='home'),
]
