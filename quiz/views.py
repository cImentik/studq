from django.shortcuts import render
from django.http import HttpResponse

from models import Unit

# Create your views here.


def index(request):
    unit_list = Unit.objects.all()
    context = {'unit_list': unit_list}
    return render(request, 'quiz/index.html', context)
