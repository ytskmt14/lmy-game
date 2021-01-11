import random
import math
from typing import List

from django.contrib.auth import logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, LogoutView)
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import LoginForm
from .models import Question, Employee, NamePlateList

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
                respondence_list = random.sample(participants, 3)
            else:
                respondence_list = random.sample(participants, len(participants))
            # 回答者フラグの立っている社員のフラグをおろす
            past_respondences = Employee.objects.filter(is_respondent=True)
            for past_respondence in past_respondences:
                past_respondence.is_respondent = False
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
            # 回答者を取得
            respondent_users = request.POST.getlist('respondence')
            # 正解者を取得
            correct_users = request.POST.getlist('correct')
            # ログインユーザ
            login_user = request.user

            # 参加者へのポイント付与
            _grant_point_to_participant(respondent_users, correct_users)
            # 回答者へのポイント付与
            _grant_point_to_respondent(correct_users)

            # 現在の回答者を過去の回答者とする
            respondences = Employee.objects.filter(username__in=respondent_users)
            for respondence in respondences:
                respondence.is_respondent = False
                respondence.was_respondent = True
                respondence.save()

            respondences_info = [respondence for respondence in respondences]
            context = {
                'is_admin': is_admin,
            }
    return render(request, "lmygame/selection.html", context)

@login_required
def name_plate_list(request):
    """
    手札一覧画面に対応するview
    """
    # ログインユーザ取得（社員番号）
    login_username = request.user
    login_user = Employee.objects.get(username=login_username)
    point = login_user.point
    # 手札確定済フラグ
    is_fixed_list = Employee.objects.get(username=login_username).is_fixed_list

    if request.method == 'GET':
        # ログインユーザが手札確定済かチェック
        if is_fixed_list:
            # 手札確定済の場合
            # DBから手札を取得
            name_plate_objects = NamePlateList.objects.filter(belong_user=login_user).values('emp_number')
            # 画面表示用のデータ作成
            username_list = [name_plate['emp_number'] for name_plate in name_plate_objects]
            name_plate_list = [Employee.objects.get(username=username) for username in username_list]
        else:
            # 手札確定済でない場合
            name_plate_list = _get_name_plate(login_user)

    elif request.method == 'POST':
        if 'reselect' in request.POST:
            # 手札を選び直すボタン押下時
            name_plate_list = _get_name_plate(login_user)

        elif 'fix' in request.POST:
            # 手札を確定するボタン押下時
            is_fixed_list = True
            # ログインユーザの手札確定済フラグをONにする
            Employee.objects.filter(username=login_username).update(is_fixed_list=is_fixed_list)
            # DBから手札を取得
            name_plate_objects = NamePlateList.objects.filter(belong_user=login_user).values('emp_number')
            # 画面表示用のデータ作成
            username_list = [name_plate['emp_number'] for name_plate in name_plate_objects]
            name_plate_list = [Employee.objects.get(username=username) for username in username_list]

    context = {
        'name_plate_list': name_plate_list,
        'is_fixed_list': is_fixed_list,
        'point': point,
    }
    return render(request, "lmygame/name_plate_list.html", context)


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
    if request.method == 'GET':
        # 所持ポイントの高い20人分のデータを取得
        rank_users = Employee.objects.all().order_by('-point')[0:20]
        # 最高ポイントを取得
        max_point = rank_users[0].point
        if max_point == 0:
            bar_length_list = [0] * 20
        else:
            # プログレスバーに表示する長さを算出
            bar_length_list = [math.floor(user.point / max_point * 100) for user in rank_users]

        context = {
            'rank_users': rank_users,
            'max_point': max_point,
            'bar_length_list': bar_length_list,
        }

    return render(request, "lmygame/result.html", context)


def _get_name_plate(login_user: Employee):
    """
    ユーザの手札を決定する
    """
    # DBの状態をリセット
    NamePlateList.objects.filter(belong_user=login_user).delete()
    # 社員の一覧を取得
    all_employee = Employee.objects.exclude(username=login_user.username).values('username')
    # 社員番号のリストを作成
    all_employee_username_list = [employee['username'] for employee in all_employee]
    # ランダムに20名選択
    selected_employee = random.sample(all_employee_username_list, 20)
    # DBに登録
    name_plate_list_objects = []
    for emp_number in selected_employee:
        name_plate_list_objects.append(
            NamePlateList(
                belong_user=login_user,
                emp_number=emp_number
            )
        )
    NamePlateList.objects.bulk_create(name_plate_list_objects)
    # 表示用データを作成
    return [Employee.objects.get(username=username) for username in selected_employee]


def _grant_point_to_participant(respondent_users: List[str], correct_users: List[str]):
    """
    参加者へのポイント付与
    """
    # 回答者を手札に持つユーザを取得
    name_plate_list = NamePlateList.objects.filter(emp_number__in=respondent_users)
    for name_plate in name_plate_list:
        # ポイント加算するユーザを取得
        winner = Employee.objects.get(username=name_plate.belong_user)
        # 1pt付与
        winner.point += 1
        if name_plate.emp_number in correct_users:
            # 正解していたらさらに2pt付与
            winner.point += 2
        winner.save()

def _grant_point_to_respondent(correct_users: List[str]):
    """
    回答者へのポイント付与
    """
    #【回答者への付与タイミング】
    # 問題に正解する → +3pt
    for correct_user in correct_users:
        winner = Employee.objects.get(username=correct_user)
        winner.point += 3
        winner.save()
