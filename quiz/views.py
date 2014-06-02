from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from models import Unit, Staff, Question, Answer, Quiz

# Create your views here.


def index(request):
    unit_list = Unit.objects.order_by("name")
    staff_list = {}
    for unit in unit_list:
        staff_list[unit.name] = Staff.objects.filter(unit_id=unit.id)
    context = {'staff_list': staff_list}
    return render(request, 'quiz/index.html', context)


def quiz(request, staff_id):
    """
    try:
        staff = Staff.objects.get(pk=staff_id)
    except Staff.DoesNotExist:
        raise Http404
    """
    staff = get_object_or_404(Staff, pk=staff_id)
    if staff.available:
        #questions = Question
        squiz = Quiz.objects.filter(staff_id=staff_id)
        args = {'staff': staff,
                'quiz': squiz}
        return render(request, 'quiz/quiz.html', args)
    else:
        raise Http404