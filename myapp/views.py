import requests

from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup

from .models import Search


BASE_CRAIGLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'


# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')

    save_to_db = Search.objects.create(search=search)
    save_to_db.save()

    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text

    soup = BeautifulSoup(data, features='html.parser')
    posts_list = soup.find_all('li', {'class': 'result-row'})

    post_title = posts_list[0].find(class_='result-title').text
    post_url = posts_list[0].find('a').get('href')
    post_price = posts_list[0].find(class_='result-price').text
    print(post_title)
    print(post_url)
    print(post_price)

    context = {
        'search': search
    }
    return render(request, 'myapp/index.html', context)
