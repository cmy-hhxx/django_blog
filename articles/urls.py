from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('articles_list/', views.articles_list, name='articles_list')
]
