from django.shortcuts import render, get_object_or_404
from .models import News
from django.http import HttpRequest, HttpResponse


def home(request: HttpRequest) -> HttpResponse:
    news = News.objects.all().order_by('-publication_date')
    return render(request, 'news/home.html', {'news': news})


def news_detail(request: HttpRequest, pk: int) -> HttpResponse:
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'news': news})
