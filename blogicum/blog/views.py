from django.shortcuts import render, get_object_or_404
import datetime

from blog.models import Category
from blog.models import Post


def index(request):
    template_name = 'blog/index.html'
    post_list = Post.objects.all().filter(is_published=True,
                                          category__is_published=True,
                                          pub_date__lte=datetime.datetime.now()
                                          )[0:5]
    context = {
        'post_list': post_list
    }
    return render(request, template_name, context)


def post_detail(request, posts_id):
    post = get_object_or_404(
        Post.objects.all().filter(
            is_published=True,
            pub_date__lte=datetime.datetime.now(),
            category__is_published=True
        ), pk=posts_id)
    context = {
        'post': post
    }
    return render(request, 'blog/detail.html', context)


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
    context = {'post_list': post_list, 'category': category}
    return render(request, 'blog/category.html', context)
