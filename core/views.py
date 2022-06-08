from django.shortcuts import render, redirect, get_object_or_404
from .models import Categories, Articles, Videos
from django.core.paginator import Paginator
import requests, json
from django.utils import timezone

MAX_PAGE = 8
LIST_CITIES = [
    {'name': 'Ош', 'id': 8666},
    {'name': 'Баткен', 'id': 43738},
    {'name': 'Чүй', 'id': 8650}, 
    {'name': 'Жалал-абад', 'id': 8655}, 
    {'name': 'Нарын', 'id': 8663},
    {'name': 'Талас', 'id': 8668}, 
    {'name': 'Ысык-көл', 'id': 8654},
]


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
    
    article = get_object_or_404(Articles, id=id)
    article.views += 1
    article.save()

    context = {
        'article': article,
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


def praytimes(request, id):
    request_id = f'praytime_{id}'
    if request.session.get(request_id, None) is None:
        response = requests.get('https://namaztimes.kz/api/praytimes', params={'id': id, 'type': 'json'})
        if response.status_code == 200:
            for city in LIST_CITIES:
                if id == city['id']:
                    city_name = city['name']
                    break
            data = response.json()
            request.session[request_id] = [data, city_name, str(timezone.now().date())]
            context = {
                'city_name': city_name,
                'data': data,
            }
            return render(request, 'praytime.html', context)
        return render(request, 'praytime.html', {'error': True, 'status': response.status_code})
    elif request.session[request_id][2] != str(timezone.now().date()):
        request.session[request_id] = None
        return redirect(f'/praytimes/{id}/')
    else:
        context = {
                'city_name': request.session[request_id][1],
                'data': request.session[request_id][0],
        }
    return render(request, 'praytime.html', context)    
        

def allPraytimes(request):
    if request.session.get('praytimes', None) is None:
        list_of_data = []
        for city in LIST_CITIES:
            response = requests.get('https://namaztimes.kz/api/praytimes', params={'id': city['id'], 'type': 'json'})
            if response.status_code == 200:
                temp = response.json()
                temp['city'] = city['name']
                list_of_data.append(temp)
            else:
                return render(request, 'list_praytime.html', {'error': True, 'status': response.status_code})
        request.session['praytimes'] = [list_of_data, str(timezone.now().date())]
        return render(request, 'list_praytime.html', {'list_of_data': list_of_data})
    elif request.session['praytimes'][1] != str(timezone.now().date()):
        request.session['praytimes'] = None
        return redirect('/praytimes/')
    else:
        context = {
                'list_of_data': request.session['praytimes'][0],
        }
        return render(request, 'list_praytime.html', context)

    

# Create your views here.
