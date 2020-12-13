from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee, Question, NamePlateList
from django.utils.translation import gettext, gettext_lazy as _
#############################
# Employee モデル（Users拡張）#
############################

def enable_is_participant(modeladmin, request, queryset):
    """
    参加者フラグを立てる
    """
    queryset.update(is_participant=True)
enable_is_participant.short_description = "参加者フラグを立てる"

def unable_is_participant(modeladmin, request, queryset):
    """
    参加者フラグをおろす
    """
    queryset.update(is_participant=False)
unable_is_participant.short_description = "参加者フラグをおろす"

def unable_is_respondent(modeladmin, request, queryset):
    """
    回答者フラグをおろす
    """
    queryset.update(is_respondent=False)
unable_is_respondent.short_description = "回答者フラグをおろす"

def unable_was_respondent(modeladmin, request, queryset):
    """
    回答済フラグをおろす
    """
    queryset.update(was_respondent=False)
unable_was_respondent.short_description = "回答済フラグをおろす"

def reset_init_status(modeladmin, request, queryset):
    """
    初期状態に戻す
    """
    # 参加者フラグ、回答者フラグ、回答済フラグをおろす
    queryset.update(is_respondent=False, was_respondent=False, is_participant=False)

reset_init_status.short_description = "初期状態に戻す"

class CustomUserAdmin(UserAdmin):

    list_display = ('username', 'first_name', 'last_name', 'point', 'is_respondent', 'was_respondent', 'is_participant')

    fieldsets = (
        (None, {'fields': ('username', 'is_admin', 'password')}),
        (_('Personal info'), {'fields': ('profile_img', 'first_name', 'last_name', 'department', 'position')}),
        (_('ゲーム情報'), {'fields': ('point', 'is_respondent', 'was_respondent', 'is_participant', )})
    )

    actions = [enable_is_participant, unable_is_participant, unable_is_respondent, unable_was_respondent, reset_init_status]

admin.site.register(Employee, CustomUserAdmin)
##################
# Question モデル #
##################
def clear_all_is_selected(modeladmin, request, queryset):
    """
    選択済フラグをすべておろす
    """
    queryset.update(is_selected=False)

clear_all_is_selected.short_description = "選択済フラグを解除する"

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'is_selected')
    actions = [clear_all_is_selected]
    fieldsets = [
        (None, {'fields': ['content', 'is_selected', 'question_img', 'answer_img']}),
    ]

admin.site.register(Question, QuestionAdmin)

#######################
# NamePlateList モデル #
#######################

class NamePlateListAdmin(admin.ModelAdmin):
    list_display = ('id', 'belong_user', 'emp_number')

admin.site.register(NamePlateList, NamePlateListAdmin)
