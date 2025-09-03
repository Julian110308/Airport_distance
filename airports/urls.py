from django.urls import path
from . import views

app_name = 'airports'

urlpatterns = [
    path('', views.airport_distance_view, name='airport_distance'),
    path('calculate/', views.calculate_distance, name='calculate_distance'),
    path('get_airports/', views.get_example_airports, name='get_example_airports'),  # Nueva ruta agregada
]