from django.shortcuts import render
from django.http import HttpResponse
from .models import ArticlePost

def articles_list(request):
    # take out all the articles
    articles = ArticlePost.objects.all()

    # deliver the articles to the templates
    context = {'articles': articles}

    # load the templates and return context object
    return render(request, 'articles/list.html', context)


