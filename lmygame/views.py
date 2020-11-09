from django.shortcuts import render

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, LogoutView)
from .forms import LoginForm
from .models import Question, Choice, Employee

class Login(LoginView):
    """
    ログイン画面に対応するview
    """
    form_class = LoginForm
    template_name = 'lmygame/login.html'

login = Login.as_view()

class Logout(LoginRequiredMixin, LogoutView):
    """
    ログアウト機能に対応するview
    """
    template_name = 'lmygame/login.html'

logout = Logout.as_view()

@login_required
def index(request):
    """
    TOP画面に対応するview
    """
    if request.method == 'GET':
        pass
    return render(request, "lmygame/index.html")

@login_required
def selection(request):
    """
    回答者選出画面に対応するview
    """
    return render(request, "lmygame/selection.html")

@login_required
def name_plate_list(request):
    """
    手札一覧画面に対応するview
    """
    return render(request, "lmygame/name_plate_list.html")

@login_required
def question(request):
    """
    問題&選択肢画面に対応するview
    """
    if request.method == 'GET':
        question = Question.objects.filter(is_selected=False).order_by('question_id').first()
        choices = Choice.objects.filter(question__question_id=question.question_id)
        context = {'question': question, 'choices': choices}
        return render(request, "lmygame/question.html", context)
    elif request.method == 'POST':
        pass

    return render(request, "lmygame/question.html")

@login_required
def result(request):
    """
    最終結果表示画面に対応するview
    """
    return render(request, "lmygame/result.html")
