import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect


def index(request):
    return render(request, 'main/index.html')


@csrf_protect
def webscraping(request):
    if request.method == "POST":

        url = request.POST.get('url')
        templ = request.POST.get('ck2')

        if existUrl(url):
            return render(request, 'main/webscraping.html', { 'weburl':url, 'templ':templ })
        else:
            return render(request, 'main/index.html')

def existUrl(url):
    try:
        requests.get(url)
        return True
    except:
        return False