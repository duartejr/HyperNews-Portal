from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings
import json
import datetime
import random


def get_news():
    with open(settings.NEWS_JSON_PATH, 'r', encoding='utf-8') as json_file:
        news = json.load(json_file)
    return news


def get(request, *args, **kwargs):
    return redirect('/news/')


class WelcomePage(View):
    pass


class NewsView(View):
    template_name = 'news_template.html'

    def get(self, request, link, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, 'r', encoding='utf-8') as json_file:
            for news in json.load(json_file):
                if news['link'] == int(link):
                    return render(request, self.template_name,
                                  {'news_dict': news})


class MainPage(View):
    template_name = "main_page_template.html"
    news = get_news()

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        if query:
            news_search_array = list(filter(lambda x: query in x['title'],
                                            self.news))
            return render(request, self.template_name,
                          {'news_array': news_search_array})

        with open(settings.NEWS_JSON_PATH, 'r', encoding='utf-8') as json_file:
            return render(request, self.template_name,
                          {'news_array': json.load(json_file)})


class CreateNews(View):
    template_name = "create_news_template.html"
    dt = datetime.datetime.now()
    date = dt.strftime('%Y-%m-%d %H:%M:%S')
    adress = int(dt.strftime("%Y%m%d%H%m%S"))

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        news = get_news()

        news_dict = {
            "created": self.date,
            "text": request.POST.get("text"),
            "title": request.POST.get("title"),
            "link": self.adress
        }

        if news_dict not in news:
            news.append(news_dict)

        with open(settings.NEWS_JSON_PATH, 'w', encoding='utf-8') as json_file:
            json.dump(news, json_file)

        return redirect("/news/")

