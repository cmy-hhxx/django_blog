from django.shortcuts import render
from django.http import HttpResponse
from .models import ArticlePost
import markdown
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ArticlePostForm
from django.contrib.auth.models import User

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

def article_create(request):
    if request.method == "POST":
        # fill the data into the form
        article_post_form = ArticlePostForm(data=request.POST)

        # judge if the data satisfy the model
        if article_post_form.is_valid():
            # save but not commit
            new_article = article_post_form.save(commit=False)

            # assgin author id=1
            new_article.author = User.objects.get(id=1)

            #save to the sqllite
            new_article.save()

            # return to the articles list
            return redirect("articles:articles_list")

        else:
            return HttpResponse("表单内容有误，请重新填写")

    else:
        article_post_form = ArticlePostForm()

        context = {'article_post_form':article_post_form}

        return render(request, 'articles/create.html', context)


def article_delete(request, id):
    # take out the detailed article
    article = ArticlePost.objects.get(id=id)

    # delete the article
    article.delete()

    # return the articles_list
    return redirect("articles:articles_list")


def article_csrf_avoidance_delete(request, id):
    if request.method == "POST":
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("articles:articles_list")
    else:
        return Httpresponse("仅支持post请求")



