from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, LogoutView)
from .forms import LoginForm

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

def index(request):
    """
    TOP画面に対応するview
    """
    return render(request, "lmygame/index.html")

def selection(request):
    """
    回答者選出画面に対応するview
    """
    return render(request, "lmygame/selection.html")

def name_plate_list(request):
    """
    手札一覧画面に対応するview
    """
    return render(request, "lmygame/name_plate_list.html")

def question(request):
    """
    問題&選択肢画面に対応するview
    """
    return render(request, "lmygame/question.html")

def result(request):
    """
    最終結果表示画面に対応するview
    """
    return render(request, "lmygame/result.html")
