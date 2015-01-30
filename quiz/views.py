# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, Http404
from django.core.context_processors import csrf
import json
from django.db import connection
from django.db.models import Avg, Max, Min, Count, Sum, QuerySet
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

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

    if request.method == 'POST':
        form = SimpleForm(request.POST, an=an, q=question.id)
        if form.is_valid():
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


def quiz(request, staff_id, question_id=1):
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
        current = Current.objects.get(session_key=s, staff=staff, question=question)
    except Current.DoesNotExist:
        current = Current(session_key=s, staff=staff, question=question)

    currents_ids = list(Current.objects.filter(session_key=s, staff=staff).values_list('question_id', flat=True))
    questions_ids = Question.objects.all().exclude(pk__in=currents_ids).values_list('id', flat=True)

    if len(questions_ids) > 0:
        if request.method == 'POST':
            mform = CurrentForm(request.POST, instance=current, qc=question.content)
            if mform.is_valid():
                #если форма заполнена и корректна
                mform.save()
                if (int(question_id) in questions_ids) and (len(questions_ids) > 1):
                    questions_ids = list(questions_ids)
                    questions_ids.remove(int(question_id))
                return redirect('quiz', staff_id=staff_id, question_id=questions_ids[0])
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
    content['staff_id'] = staff.id
    content['select_error'] = select_error
    content['questions'] = questions_ids
    content['currents_ids'] = currents_ids
    content['end'] = end

    return render_to_response('quiz/mform.html', content)


def end(request):
    logout(request)
    response = redirect('/')
    return response


@login_required
def reports(request):
    user = request.user
    is_user = False
    if user.is_authenticated():
        is_user = True
    staffs = Current.objects.values_list('staff__id', flat=True).distinct()
    unit_list = Unit.objects.all()
    staff_list = {}
    for unit in unit_list:
        staff_list[unit.name] = Staff.objects.filter(unit_id=unit.id, pk__in=staffs).order_by("name")
    content = {
        'staff_list': staff_list,
        'is_user': is_user,
        'q': connection.queries,
        'staffs': staffs,
    }
    return render_to_response('quiz/reports.html', content)


@login_required
def report(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    questions = Question.objects.all().values('id', 'content')
    answer_weights = Answer.objects.all().values_list('weight', flat=True)
    #query = Answer.objects.all()
    data = {}
    q = connection
    question_result = {}
    for question in questions:
        results = Current.objects.filter(question_id=question['id'], staff_id=staff_id).values_list \
            ('answer__weight', flat=True).order_by('answer__weight')
        xaxis = frequency(answer_weights, results).keys()
        yaxis = frequency(answer_weights, results).values()
        data[question['id']] = {
            'results': results,
            'content': question['content'],
            'frequency': frequency(answer_weights, results),
            'xaxis': tuple(xaxis),
            'yaxis': tuple(yaxis),
            'mean': mean(results),
            'std': std(results),
            'median': median(results),
        }
    content = {
        'staff_name': staff.name,
        'unit_name': staff.unit.name,
        #'query': query.query,
        #'res': results,
        'data': data,
        'q': q,
    }
    return render_to_response('quiz/report.html', content)


def frequency(answer_weights, answers):
    """Вычисление частоты - БЫДЛОКОД!!!!!!1111одынодын"""
    data_dictionary = dict()
    counter = 0
    for weight in answer_weights:
        if weight in answers:
            for a in answers:
                if a == weight:
                    counter += 1
        else:
            counter = 0
        data_dictionary[weight] = counter
        counter = 0
    return data_dictionary


def mean(answers):
    """Вычисление среднеарифмитичского значения"""
    if len(answers) < 1:
        result = 0
    else:
        result = round(sum(answers)/len(answers), 2)
    return result


def std(answers):
    """Вычисление среднеквадратичного отклонения"""
    m = mean(answers)
    numerator = sum((x-m)**2 for x in answers)
    l = len(answers)
    if l < 2:
        results = 0
    else:
        results = numerator/l
        results = round((results**0.5), 2)
    return results


def median(answers):
    """Вычисление медианы"""
    lenght = len(answers)
    index = ((lenght-1) // 2)
    if lenght % 2 == 0:
        result = (answers[index]+answers[index+1])/2.0
    else:
        result = answers[index]
    return  result