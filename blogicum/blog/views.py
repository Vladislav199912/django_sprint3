from django.shortcuts import render, get_object_or_404

import datetime

from blog.models import Category, Post

from blog.constans import PER_AGE


def index(request):
    post_list = Post.objects.all().filter(is_published=True,
                                          category__is_published=True,
                                          pub_date__lte=datetime.datetime.now()
                                          )[:PER_AGE]
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.all().filter(
            is_published=True,
            pub_date__lte=datetime.datetime.now(),
            category__is_published=True
        ), pk=post_id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
        )
    post_list = Post.objects.select_related(
        'category'
        ).filter(
        category__slug=category_slug,
        pub_date__lte=datetime.datetime.now(),
        is_published=True,
        category__is_published=True
        )
    return render(request, 'blog/category.html',
                  {'post_list': post_list, 'category': category})
