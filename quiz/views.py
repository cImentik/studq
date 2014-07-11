# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator
import json

from quiz.forms import ContactForm, SimpleForm

from models import Unit, Staff, Question, Answer, Quiz

# Create your views here.


def index(request):
    unit_list = Unit.objects.order_by("name")
    staff_list = {}
    for unit in unit_list:
        staff_list[unit.name] = Staff.objects.filter(unit_id=unit.id)
    context = {'staff_list': staff_list}
    return render(request, 'quiz/index.html', context)


def quiz(request, staff_id, page_number=1):
    #assert False
    ##TODO: Ограничение на количество страниц
    staff = get_object_or_404(Staff, pk=staff_id)
    if staff.available:
        squiz = Quiz.objects.filter(staff_id=staff_id)
        content = []
        for q in squiz:
            question = Question.objects.get(content=q.question_id)
            answers = Answer.objects.filter(question_id=question.id)
            pages = {'question': question.content,
                     'answers': answers,
                     }
            content.append(pages)
        current_page = Paginator(content, 1)
        args = {'staff': staff,
                'quiz': squiz,
                'content': current_page.page(page_number)}
        return render(request, 'quiz/quiz.html', args)
    else:
        raise Http404


def forms(request, q_id):
    m = ''
    args = {}
    p = get_object_or_404(Question, pk=q_id)
    try:
        selected_choice = p.answer_set.get(pk=request.POST['choice'])
    except (KeyError, Answer.DoesNotExist):
        answers = Answer.objects.filter(question_id=q_id)
        args = {'m': m,
                'answers': answers
                }
        return render(request, 'quiz/forms.html', args)
    else:
        answers = Answer.objects.filter(question_id=q_id)
        m = 'OK'
        args = {'m': selected_choice,
                'answers': answers
        }
        return render(request, 'quiz/forms.html', args)


def form(request):
    m = ''
    an = []
    answers = Answer.objects.filter(question_id=1)
    for ans in answers:
        an.append((ans.content, ans.content))

    if request.method == 'POST': # If the form has been submitted...
        form = SimpleForm(request.POST, an=an) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            #return HttpResponseRedirect('/form/') # Redirect after POST
            return render(request, 'quiz/form.html', {'form': form})
    else:
        form = SimpleForm({}, an=an) # An unbound form
    return render(request, 'quiz/form.html', {
        'form': form,
    })


def jform(request):
    if request.is_ajax():
        message = 'Hello world!'
    else:
        message = 'Hello'
    return HttpResponse(message)


def ajax_test(request):
    #context = {}
    try:
        data = request.POST['text'].strip()
    except:
        context = '{ "new-text": "error" }'
    else:
        context = json.dumps({"new-text": data[::-1]})
    return HttpResponse(context)