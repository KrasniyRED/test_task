from django.shortcuts import render, get_object_or_404
from .models import News, Comments
from .serializers import NewsSerializer, CommentSerializer
from django.http import HttpRequest, HttpResponse
from rest_framework import generics, request, response, status

class GenericNewsView(generics.GenericAPIView):
    queryset = News.objects.all().order_by('-publication_date')
    serializer_class = NewsSerializer

    def get(self, *args, **kwargs) -> response.Response:
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return response.Response(serializer.data)

    def post(self, request: request.Request) -> response.Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(status=status.HTTP_201_CREATED)

    def patch(
        self, request: request.Request, *args, **kwargs
    ) -> response.Response:
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)

    def delete(
        self, request: request.Request, *args, **kwargs
    ) -> response.Response:
        instance: News = self.get_object()
        instance.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class GenericCommentsView(generics.GenericAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

    def get(self, *args, **kwargs) -> response.Response:
        serializer = self.get_serializer(
            self.get_queryset().filter(related_news=kwargs['pk']), many=True
        )
        return response.Response(serializer.data)

    def post(
        self, request: request.Request, pk: int, *args, **kwargs
    ) -> response.Response:
        request.data.update({'related_news': pk})
        serializer: CommentSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(status=status.HTTP_201_CREATED)

    def patch(
        self, request: request.Request, comment_pk: int, *args, **kwargs
    ) -> response.Response:
        instance = get_object_or_404(Comments, id=comment_pk, related_news=kwargs['pk'])
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)

    def delete(
        self, request: request.Request, comment_pk: int, *args, **kwargs
    ) -> response.Response:
        instance = get_object_or_404(Comments, id=comment_pk, related_news=kwargs['pk'])
        instance.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


def home(request: HttpRequest) -> HttpResponse:
    news = News.objects.all().order_by('-publication_date')
    return render(request, 'news/home.html', {'news': news})


def news_detail(request: HttpRequest, pk: int) -> HttpResponse:
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'news': news})
