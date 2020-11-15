from django.shortcuts import render

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, LogoutView)
from .forms import LoginForm, ChoiceForm
from .models import Question, Choice, Employee, Answer

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
    # 問題取得
    question = Question.objects.filter(is_selected=False).order_by('question_id').first()
    # ユーザのステータス取得
    is_admin = request.user.is_admin
    is_respondent = request.user.is_respondent
    # 答え表示フラグ
    is_disp_answer = False

    if request.method == 'GET':
        choices, form = _get_choices(question)
        context = {
            'question': question,
            'choices': choices,
            'form': form,
            'is_admin': is_admin,
            'is_respondent': is_respondent,
            'is_disp_answer': is_disp_answer,
        }
    elif request.method == 'POST':
        if 'selection' in request.POST:
            # 回答者選出ボタン押下時
            print('selection')
            return render(request, "lmygame/selection.html")
        elif 'answer' in request.POST:
            # 答えを表示ボタン押下時
            # 正解を取得
            answer = _get_correct_choice(question).get().choice_text
            # 答え表示フラグをONにする
            is_disp_answer = True
            # 画面を表示する
            context = {
                'question': question,
                'answer': answer,
                'is_admin': is_admin,
                'is_respondent': is_respondent,
                'is_disp_answer': is_disp_answer,
            }
            print('answer')
        elif 'next' in request.POST:
            # 次の問題へボタン押下時
            # 現在の問題に選択済フラグを立てる
            question.is_selected = True
            question.save()
            # 次の問題を取得する
            next_question = Question.objects.filter(is_selected=False).order_by('question_id').first()
            # 問題に対応する選択肢を取得する
            choices, form = _get_choices(next_question)
            # 画面を表示する
            context = {
                'question': next_question,
                'choices': choices,
                'form': form,
                'is_admin': True,
                'is_respondent': False,
                'is_disp_answer': False,
            }
        elif 'respond' in request.POST:
            # 回答するボタン押下時
            # Answerモデルにデータ登録
            respondent_id = request.user.username
            answer = request.POST['choice']
            Answer.objects.create(respondent=respondent_id, answer=answer, question=question)
            # 回答者の回答者フラグ(is_respondent)と回答済フラグ(was_respondent)を更新
            respondent = Employee.objects.filter(username=respondent_id).get()
            respondent.is_respondent = False
            respondent.was_respondent = True
            respondent.save()
            # 画面表示用のデータ取得
            choices, form = _get_choices(question)
            context = {
                'question': question,
                'choices': choices,
                'form': form,
                'is_admin': respondent.is_admin,
                'is_respondent': respondent.is_respondent,
                'is_disp_answer': is_disp_answer,
            }

    return render(request, "lmygame/question.html", context)

@login_required
def result(request):
    """
    最終結果表示画面に対応するview
    """
    return render(request, "lmygame/result.html")


def _get_choices(question):
    """
    問題に紐づく選択肢を取得する関数（private）
    """
    choices = Choice.objects.filter(question__question_id=question.question_id)
    form = ChoiceForm()
    form.fields['choice'].queryset = Choice.objects.filter(question__question_id=question.question_id)
    return choices, form

def _get_correct_choice(question):
    """
    問題の正解の選択肢のみを取得する関数(private)
    """
    choice = Choice.objects.filter(question__question_id=question.question_id).filter(is_correct=1)
    return choice