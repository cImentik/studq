# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator

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
    """
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
    """
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