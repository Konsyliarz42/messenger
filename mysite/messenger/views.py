from django.shortcuts import render
from django.http import HttpResponse

TEMPLATES = {
    'index': "index.html"
}

def index(request):
    context = dict()

    return render(request, TEMPLATES['index'], context)