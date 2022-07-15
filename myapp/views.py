from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
from datetime import timedelta
# Create your views here.


def home(request):
    return render(request, 'registration/home.html')


def register(request):
    msg = None
    form = forms.RegisterUser
    if request.method == 'POST':
        form = forms.RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            msg = 'Data has been added'
    return render(request, 'registration/register.html', {'form': form, 'msg': msg})


def categories(request):
    catData = models.QuizCategory.objects.all()
    return render(request, 'registration/category.html', {'data': catData})


@login_required
def category_questions(request, cat_id):
    category = models.QuizCategory.objects.get(id=cat_id)
    question = models.QuizQuestion.objects.filter(
        category=category).order_by('id').first()
    return render(request, 'registration/category-questions.html', {'question': question, 'category': category})


@login_required
def category_questions(request, cat_id):
    category = models.QuizCategory.objects.get(id=cat_id)
    question = models.QuizQuestion.objects.filter(
        category=category).order_by('id').first()
    lastAttempt = None
    futureTime = None
    hoursLimit = 48
    countAttempt = models.UserCategoryAttempts.objects.filter(
        user=request.user, category=category).count()
    if countAttempt == 0:
        models.UserCategoryAttempts.objects.create(
            user=request.user, category=category)
    else:
        lastAttempt = models.UserCategoryAttempts.objects.filter(
            user=request.user, category=category).order_by('-id').first()
        futureTime = lastAttempt.attempt_time+timedelta(hours=hoursLimit)

        if lastAttempt and lastAttempt.attempt_time < futureTime:
            return redirect('attempt-limit')

        else:
            models.UserCategoryAttempts.objects.create(
                user=request.user, category=category)
    return render(request, 'registration/category-questions.html', {'question': question, 'category': category, 'lastAttempt': futureTime})


@login_required
def submit_answer(request, cat_id, quest_id):
    if request.method == 'POST':
        category = models.QuizCategory.objects.get(id=cat_id)

        question = models.QuizQuestion.objects.filter(
            category=category, id__gt=quest_id).exclude(id=quest_id).order_by('id').first()
        if 'skip' in request.POST:

            if question:
                quest = models.QuizQuestion.objects.get(id=quest_id)
                user = request.user
                answer = "Not Submitted"
                models.UserSubmittedAnswer.objects.create(
                    user=user, question=quest, right_answer=answer)
                return render(request, 'registration/category-questions.html', {'question': question, 'category': category})
        else:
            quest = models.QuizQuestion.objects.get(id=quest_id)
            user = request.user
            answer = request.POST['answer']
            models.UserSubmittedAnswer.objects.create(
                user=user, question=quest, right_answer=answer)
        if question:
            return render(request, 'registration/category-questions.html', {'question': question, 'category': category})
        else:
            return HttpResponse('no more question')
    else:
        return HttpResponse('Method Not allowed!!')


def attempt_limit(request):
    return render(request, 'registration/attempt-limit.html')
