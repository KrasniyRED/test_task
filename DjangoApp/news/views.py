from django.shortcuts import render, get_object_or_404
from .models import News
from .serializers import NewsSerializer
from django.http import HttpRequest, HttpResponse
from rest_framework import generics, request, response, viewsets
from rest_framework.decorators import action

class GenericNewsView(generics.GenericAPIView):
    queryset = News.objects.all().order_by('-publication_date')
    serializer_class = NewsSerializer
    
class GenericNewsViewSet(GenericNewsView,viewsets.ViewSet):
    

    def list(self,*args, **kwargs)-> response.Response:
        serializer = self.get_serializer(self.get_queryset(),many = True)
        return response.Response(serializer.data)
    
    def retrieve(self,*args, **kwargs)-> response.Response:
        serializer = self.get_serializer(self.get_object())
        return response.Response(serializer.data)
    
    def create(self,request:request.Request)-> response.Response:
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(status=200)
    
    def partial_update(self,request:request.Request,*args, **kwargs)-> response.Response:
        instance = self.get_object()
        serializer = self.get_serializer(instance, data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return response.Response(serializer.data)
    
    def destroy(self,request:request.Request,*args, **kwargs)-> response.Response:
        instance : News = self.get_object()
        instance.delete()
        return response.Response(status=204)


def home(request: HttpRequest) -> HttpResponse:
    
    news = News.objects.all().order_by('-publication_date')
    return render(request, 'news/home.html', {'news': news})


def news_detail(request: HttpRequest, pk: int) -> HttpResponse:
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'news': news})
