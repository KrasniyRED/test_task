from django.shortcuts import render, get_object_or_404, redirect
from .models import News

def home(request):
    news = News.objects.all().order_by('-publication_date')
    return render(request, 'news/home.html', {'news': news})

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'news': news})