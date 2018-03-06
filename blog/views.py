from markdown import markdown
from django.shortcuts import render, get_object_or_404, redirect
from comments.forms import CommentForm
from .models import Post, Category

# Create your views here.


def index(request):
    post_list = Post.objects.all()
    for post in post_list:
        post.body = markdown(post.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
    return render(request, 'blog/index.html', context={
        # 'title': 'welcome',
        # 'welcome': str(dir(type(Post.objects.all()))),
        'post_list': post_list,
    })


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown(post.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    comment_count = post.comment_set.count()

    return render(request,
                  'blog/detail.html',
                  context={'post': post,
                           'form': form,
                           'comment_list': comment_list,
                           'comment_count': comment_count
                           })


def archives(request, year, month):
    post_list = Post.objects.filter(
        created_time__year=year,
        created_time__month=month
    )
    for post in post_list:
        post.body = markdown(post.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
    return render(request, 'blog/index.html', context={
        # 'title': 'welcome',
        # 'welcome': str(dir(type(Post.objects.all()))),
        'post_list': post_list,
    })


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    for post in post_list:
        post.body = markdown(post.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
    return render(request, 'blog/index.html', context={'post_list': post_list})
