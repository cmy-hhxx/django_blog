from django.shortcuts import render
from django.http import HttpResponse
from .models import ArticlePost
import markdown
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from comment.models import Comment
from .models import ArticleColumn

def articles_list(request):
    # take out all the articles
    #articles_list = ArticlePost.objects.all()

    #paginator = Paginator(articles_list, 1)

    #page = request.GET.get('page')

    #articles = paginator.get_page(page)

    # deliver the articles to the templates
    #context = {'articles': articles}

    # load the templates and return context object
    #return render(request, 'articles/list.html', context)
    """if request.GET.get('order') == 'total_views':
        article_list = ArticlePost.objects.all().order_by('-total_views')
        order = 'total_views'
    else:
        article_list = ArticlePost.objects.all()
        order = 'normal'

    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # 修改此行
    context = { 'articles': articles, 'order': order }

    return render(request, 'articles/list.html', context)"""
   # 从 url 中提取查询参数
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    # 初始化查询集
    article_list = ArticlePost.objects.all()

    # 搜索查询集
    if search:
        article_list = article_list.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
                )
    else:
        search = ''

    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    # 查询集排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')

    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # 需要传递给模板（templates）的对象
    context = {
            'articles': articles,
            'order': order,
            'search': search,
            'column': column,
            'tag': tag,
            }

    return render(request, 'articles/list.html', context) 

def article_detail(request, id):
    # take out the resigned article
    article = ArticlePost.objects.get(id=id)

    comments = Comment.objects.filter(article=id)

    article.total_views += 1
    article.save(update_fields=['total_views'])

    # rendering markdown to html
    """article.body = markdown.markdown(article.body,
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.TOC',
                ])"""
    md = markdown.Markdown(
        extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)

    # deliver the article to the templates
    context = {'article': article,'toc': md.toc, 'comments': comments}

    # load the templates and return context object
    return render(request, 'articles/detail.html', context)

@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == "POST":
        # fill the data into the form
        article_post_form = ArticlePostForm(data=request.POST)

        # judge if the data satisfy the model
        if article_post_form.is_valid():
            # save but not commit
            new_article = article_post_form.save(commit=False)

            # assgin author id=1
            new_article.author = User.objects.get(id=request.user.id)
            # new_article.author = User.objects.get(id=1)

            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])

            #save to the sqllite
            new_article.save()

            article_post_form.save_m2m()

            # return to the articles list
            return redirect("articles:articles_list")

        else:
            return HttpResponse("表单内容有误，请重新填写")

    else:
        article_post_form = ArticlePostForm()

        columns = ArticleColumn.objects.all()

    context = {'article_post_form':article_post_form,'columns': columns}

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

@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    # take out the article
    article = ArticlePost.objects.get(id=id)

    if request.user != article.author:
        return HttpResponse("抱歉，无权修改")

    # jude the method
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            #article = article_post_form.save(commit=False)
            # write the new body
            article.author = User.objects.get(id=request.user.id)
            article.title = request.POST['title']

            article.body = request.POST['body']

            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None

            article.save()


            return redirect("articles:article_detail", id=id)

        else:
            return HttpResponse("表单内容有误，请重新填写")

    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context = {'article': article, 'article_post_form': article_post_form, 'columns': columns}
        return render(request, 'articles/update.html', context)

