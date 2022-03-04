from django.shortcuts import render
from django.db.models import F
from django.views.generic import View
from .models import Article


class ArticleListView(View):

    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        context = {
            'articles': articles
        }
        return render(request, 'blog/list_of_articles.html', context=context)


class ArticleDetailView(View):

    def get(self, request, *args, **kwargs):
        article = Article.objects.filter(slug=kwargs['slug'])
        context = {
            'article': article.first()
        }
        article.update(views_counter=F('views_counter')+1)
        return render(request, 'blog/article_detail.html', context=context)
