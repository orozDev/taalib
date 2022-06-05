from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from .models import Categories, Articles, Videos
from django.core.paginator import Paginator

MAX_PAGE = 3

def main(request):

    articles = Articles.objects.all()
    pagin = Paginator(articles, MAX_PAGE)
    page = request.GET.get('page', None)
    if page is None:
        articles_page = pagin.get_page(1)
    else:
        articles_page = pagin.get_page(page)
    
    context = {
        'articles': articles_page,
    }

    return render(request, 'main.html', context)


def getByCategory(request, id):

    articles = Articles.objects.filter(is_published=True, categories__id=id)
    pagin = Paginator(articles, MAX_PAGE)
    page = request.GET.get('page', None)

    if page is None:
        articles_page = pagin.get_page(1)
    else:
        articles_page = pagin.get_page(page)
    

    context = {
        'articles': articles_page,
        'category': get_object_or_404(Categories, id=id)
    }

    return render(request, 'filter_article.html', context)



def getItem(request, id):
    
    context = {
        'article': get_object_or_404(Articles, id=id),
    }

    return render(request, 'item.html', context)


def getVideos(request):

    viedeos = Videos.objects.filter(is_published=True)
    pagin = Paginator(viedeos, MAX_PAGE)
    page = request.GET.get('page', None)

    if page is None:
        viedeos_page = pagin.get_page(1)
    else:
        viedeos_page = pagin.get_page(page)
    

    context = {
        'videos': viedeos_page,
    }

    return render(request, 'videos.html', context)


def getByCategoryVideos(request, id):
    viedeos = Videos.objects.filter(is_published=True, categories__id=id)
    pagin = Paginator(viedeos, MAX_PAGE)
    page = request.GET.get('page', None)

    if page is None:
        viedeos_page = pagin.get_page(1)
    else:
        viedeos_page = pagin.get_page(page)
    

    context = {
        'videos': viedeos_page,
        'category': get_object_or_404(Categories, id=id)
    }

    return render(request, 'filter_videos.html', context)



def search_article(request):
    title = request.GET.get('search', None)
    context = {
        'articles': Articles.objects.filter(title__icontains=title),
        'search': title,
    }

    return render(request, 'main.html', context)

def search_video(request):
    title = request.GET.get('search', None)
    context = {
        'videos': Videos.objects.filter(title__icontains=title),
        'search': title,
    }

    return render(request, 'videos.html', context)
# Create your views here.
