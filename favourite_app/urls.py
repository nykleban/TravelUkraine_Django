from django.urls import path

from favourite_app import views

urlpatterns = [
    path('', views.favourite_list, name='favourite_list'),
    path('add/<int:place_id>/', views.add_to_favourite, name='add_to_favourite'),
    path('delete/<int:place_id>/', views.delete_from_favourite, name='delete_from_favourite'),
]
