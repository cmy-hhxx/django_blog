from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Comment
from articles.models import ArticlePost
from .forms import CommentForm

# 文章评论
@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(ArticlePost, id=article_id)

    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                new_comment.parent_id = parent_comment.get_root().id
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                return HttpResponse('200 OK')

            new_comment.save()

            redirect_url = article.get_absolute_url() + '#comment_elem_' + str(new_comment.id)

            return redirect(redirect_url)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    elif request.method == "GET":
        comment_form = CommentForm()
        context = {
                'comment_form': comment_form,
                'article_id': article_id,
                'parent_comment_id': parent_comment_id,
            }
        return render(request, 'comment/reply.html', context)
    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接受POST/GET请求。")
