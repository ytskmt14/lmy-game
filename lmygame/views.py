import random

from django.contrib.auth import logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, LogoutView)
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import LoginForm
from .models import Question, Employee

class Login(LoginView):
    """
    ログイン画面に対応するview
    """
    form_class = LoginForm
    template_name = 'lmygame/login.html'
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        user = Employee.objects.get(username=username)
        user.is_participant = True
        user.save()
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

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
    is_admin = request.user.is_admin

    if request.method == 'GET':
        respondences = Employee.objects.filter(is_respondent=True).values('username')
        respondences_info = [Employee.objects.get(username=respondence['username']) for respondence in respondences]
        context = {
            'is_admin': is_admin,
            'respondences_info': respondences_info,
        }
    elif request.method == 'POST':
        if 'selection' in request.POST:
            #############################
            # 回答者を選ぶボタン押下時の処理 #
            #############################
            # 参加者、かつ回答済でない人をリスト化
            participants = Employee.objects.filter(is_participant=True).filter(was_respondent=False).values('username')
            # リストからランダムに3名選出
            participants = [participant['username'] for participant in participants]
            respondence_list = []
            if len(participants) >= 3:
                respondence_list = random.sample(participants, 2)
                # respondence_list = random.sample(participants, 3)
            else:
                respondence_list = random.sample(participants, len(participants))
            # 回答者フラグの立っている社員のフラグをおろす
            past_respondences = Employee.objects.filter(is_respondent=True)
            for past_respondence in past_respondences:
                past_respondence.is_respondent = False
                past_respondence.was_respondent = True
                past_respondence.save()

            # 選出された社員の回答者フラグを立てる
            for username in respondence_list:
                respondent = Employee.objects.get(username=username)
                respondent.is_respondent = True
                respondent.save()

            respondences_info = [Employee.objects.get(username=username) for username in respondence_list]
            context = {
                'is_admin': is_admin,
                'respondences_info': respondences_info,
            }
        elif 'grantPoint' in request.POST:
            #############################
            # ポイント付与ボタン押下時の処理 #
            #############################
            #【参加者への付与タイミング】　
            #・ 手札の社員が回答者に選ばれる → +1pt
            #・ 手札の社員が正解する → +2pt
            #【回答者への付与タイミング】
            #・  問題に正解する → +3pt

            pass
    return render(request, "lmygame/selection.html", context)

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
    # 問題取得
    question = Question.objects.filter(is_selected=False).order_by('question_id').first()
    # ユーザのステータス取得
    is_admin = request.user.is_admin
    # 答え表示フラグ
    is_disp_answer = False

    if request.method == 'GET':
        context = {
            'question': question,
            'is_admin': is_admin,
            'is_disp_answer': is_disp_answer,
        }
    elif request.method == 'POST':
        if 'answer' in request.POST:
            # 答えを表示ボタン押下時
            # 答え表示フラグをONにする
            is_disp_answer = True
            # 画面を表示する
            context = {
                'question': question,
                'is_admin': is_admin,
                'is_disp_answer': is_disp_answer,
            }
        elif 'next' in request.POST:
            # 次の問題へボタン押下時
            # 現在の問題に選択済フラグを立てる
            question.is_selected = True
            question.save()
            # 次の問題を取得する
            next_question = Question.objects.filter(is_selected=False).order_by('question_id').first()
            # 画面を表示する
            context = {
                'question': next_question,
                'is_admin': True,
                'is_disp_answer': False,
            }

    return render(request, "lmygame/question.html", context)

@login_required
def result(request):
    """
    最終結果表示画面に対応するview
    """
    return render(request, "lmygame/result.html")
