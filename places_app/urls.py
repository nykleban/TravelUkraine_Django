from django.urls import path

from places_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('places/', views.place_list, name='place_list'),
    path('places/<int:place_id>/', views.place_detail, name='place_detail'),
    path('search/', views.search, name='search'),
    path('admin-panel/', views.admin_places, name='admin_places'),
    path('admin-panel/delete/<int:place_id>/', views.delete_place, name='delete_place'),
    path('admin-panel/create/', views.create_place, name='create_place'),
    path('admin-panel/update/<int:place_id>/', views.update_place, name='update_place'),
]
