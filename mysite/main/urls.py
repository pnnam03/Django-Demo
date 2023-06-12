from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name = 'home'),
    path('create/', views.create, name = 'create'),
    path('list/', views.list_all, name="list_all"),
    path("list/<int:id>/", views.list, name = 'list'),
]