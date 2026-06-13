from django.urls import path

from places_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('places/', views.place_list, name='place_list'),
    path('places/<int:place_id>/', views.place_detail, name='place_detail'),
    path('search/', views.search, name='search'),
]
