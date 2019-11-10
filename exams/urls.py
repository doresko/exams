from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.searchlist, name='search_results'),
    path('preferences/', views.preferences, name='preferences'),
    path('blog/<slug:problem_slug>', views.task, name='task'),
]