from django.shortcuts import render
from django.views.generic import View
from .models import TextEditor


class ArticleListView(View):

    def get(self, request, *args, **kwargs):
        articles = TextEditor.objects.all()
        context = {
            'articles': articles
        }
        return render(request, 'blog/list_of_articles.html', context=context)


class ArticleDetailView(View):

    def get(self, request, *args, **kwargs):
        article = TextEditor.objects.get()
        context = {
            'article': article
        }
        return render(request, 'blog/article_detail.html', context=context)
