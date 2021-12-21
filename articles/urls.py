from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('articles_list/', views.articles_list, name='articles_list'),
    path('article_detail/<int:id>/', views.article_detail, name='article_detail'),
    path('article_create/', views.article_create, name='article_create'),
    path('article_delete/<int:id>/', views.article_delete, name='article_delete'),
    path('article_csrf_avoidance_delete/<int:id>/', views.article_csrf_avoidance_delete, name='article_csrf_avoidance_delete'),
]
