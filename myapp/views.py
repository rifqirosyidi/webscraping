import requests

from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup

from .models import Search


BASE_CRAIGLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_CRAIGLIST_IMG = 'https://images.craigslist.org/{}_300x300.jpg'


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
    print(posts_list[0])
    post_image = posts_list[0].find()

    final_post = []

    for post in posts_list:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        post_price = post.find(class_='result-price')

        if post_price.text != '$0':
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_CRAIGLIST_IMG.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_post.append((post_title, post_url, post_price, post_image_url))


    context = {
        'search': search,
        'final_post': final_post
    }
    return render(request, 'myapp/index.html', context)
