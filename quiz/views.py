# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.context_processors import csrf
import json
from django.db import connection

from .forms import ContactForm, SimpleForm, CurrentForm

from .models import Unit, Staff, Question, Answer, Quiz, Current

# Create your views here.


def index(request):
    unit_list = Unit.objects.order_by("name")
    staff_list = {}
    for unit in unit_list:
        staff_list[unit.name] = Staff.objects.filter(unit_id=unit.id)
    context = {'staff_list': staff_list}
    return render(request, 'quiz/index.html', context)


def quiz(request, staff_id, page_number=1):
    # assert False
    # #TODO: Ограничение на количество страниц
    staff = get_object_or_404(Staff, pk=staff_id)
    if staff.available:
        content = []
        question = Question.objects.all()
        answers = Answer.objects.all()
        an = [] #answers tuple
        for q in question:
            pages = {'question': q.content,
                     'answers': answers, }
            content.append(pages)
        #current_page = Paginator(content, 1)
        args = {'staff': staff,
                #'quiz': squiz,
                # 'content': current_page.page(page_number)#
                }
        return render(request, 'quiz/quiz.html', args)
    else:
        raise Http404


def forms(request, q_id):
    q = get_object_or_404(Question, pk=q_id)
    try:
        # assert False
        selected_choice = Answer.objects.get(pk=request.POST['choice'])
    except (KeyError, Answer.DoesNotExist):
        answers = Answer.objects.all()
        args = {'question': q.content,
                'answers': answers
        }
        return render(request, 'quiz/forms.html', args)
    else:
        answers = Answer.objects.all()
        args = {'question': q.content,
                'm': selected_choice,
                'answers': answers
        }
        return render(request, 'quiz/forms.html', args)


def form(request):
    an = []
    question = Question.objects.filter(pk=1)
    answers = Answer.objects.all()
    for ans in answers:
        an.append((ans.id, ans.content))

    if request.method == 'POST':  # If the form has been submitted...
        form = SimpleForm(request.POST, an=an, q=question.id)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            # return HttpResponseRedirect('/form/') # Redirect after POST
            return render(request, 'quiz/form.html', {'form': form})
    else:
        form = SimpleForm({}, an=an, q=question[0])  # An unbound form
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
    # context = {}
    try:
        data = request.POST['text'].strip()
    except:
        context = '{ "new-text": "error" }'
    else:
        context = json.dumps({"new-text": data[::-1]})
    return HttpResponse(context)


def ajax_test2(request):
    # context = {}
    #assert False
    try:
        d = json.loads(request.POST['form'])
        data = request.POST['text'].strip()
        #f = request.POST['form']
    except:
        context = '{ "new-text": "error" }'
    else:
        context = json.dumps({"new-text": data[::-1], "f": d})
    return HttpResponse(context)


def mform(request, staff_id, question_id=1):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    s = request.session.session_key
    staff = get_object_or_404(Staff, pk=staff_id)
    question = get_object_or_404(Question, pk=question_id)
    select_error = False
    end = False
    content = {}
    content.update(csrf(request))

    try:
        current = Current.objects.get(session_key=s, staff_id=staff, question_id=question)
    except Current.DoesNotExist:
        current = Current(session_key=s, staff_id=staff, question_id=question)

    currents_ids = list(Current.objects.filter(session_key=s, staff_id=staff).values_list('question_id', flat=True))
    #currents_ids.append(question.id)
    questions_ids = Question.objects.all().exclude(pk__in=currents_ids).values_list('id', flat=True)

    if len(questions_ids) > 0:
        if request.method == 'POST':
            mform = CurrentForm(request.POST, instance=current, qc=question.content)
            if mform.is_valid():
                #если форма заполнена и корректна
                mform.save()
                #questions = Question.objects.filter(question_id=question_id)
                return redirect('mform', staff_id=staff_id, question_id=questions_ids[0])
            else:
                #если форма не заполнена или не корректна
                select_error = True
        else:
            mform = CurrentForm(instance=current, qc=question.content)
        #assert False
    else:
        mform = None
        end = True
    content['mform'] = mform
    content['con'] = connection.queries
    content['staff_name'] = staff.name
    content['select_error'] = select_error
    content['questions'] = questions_ids
    content['currents_ids'] = currents_ids
    content['end'] = end

    return render(request, 'quiz/mform.html', content)


def end(request, staff_id):
    context = {}
    return render(request, 'quiz/end.html', context)