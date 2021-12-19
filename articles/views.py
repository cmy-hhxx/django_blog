from django.shortcuts import render
from django.http import HttpResponse
from .models import ArticlePost
import markdown

def articles_list(request):
    # take out all the articles
    articles = ArticlePost.objects.all()

    # deliver the articles to the templates
    context = {'articles': articles}

    # load the templates and return context object
    return render(request, 'articles/list.html', context)

def article_detail(request, id):
    # take out the resigned article
    article = ArticlePost.objects.get(id=id)

    # rendering markdown to html
    article.body = markdown.markdown(article.body,
            extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
             ])

    # deliver the article to the templates
    context = {'article': article}

    # load the templates and return context object
    return render(request, 'articles/detail.html', context)

