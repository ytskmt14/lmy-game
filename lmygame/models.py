import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser, UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

class Employee(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('社員番号'),
        max_length=6,
        unique=True,
        help_text=_('Required. 6 digits only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    is_fixed_list = models.BooleanField(
        _('手札確定済'),
        default=False,
    )
    is_admin = models.BooleanField(
        _('運営'),
        default=False,
    )
    point = models.IntegerField(
        _('所持ポイント'),
        default=0,
    )
    is_respondent = models.BooleanField(
        _('回答者'),
        default=False
    )
    was_respondent = models.BooleanField(
        _('回答済'),
        default=False,
    )
    is_participant = models.BooleanField(
        _('参加者'),
        default=False
    )
    department = models.CharField(
        _('部署'),
        max_length=50,
        null=True,
    )
    position = models.CharField(
        _('役職'),
        max_length=50,
        null=True,
    )
    profile_img = models.ImageField(
    _('顔写真'),
    upload_to='profiles',
    blank=True,
    )

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    content = models.TextField(
        _('問題概要'),
    )
    is_selected = models.BooleanField(
        _('選択済'),
        default=False,
    )
    question_img = models.ImageField(
        _('問題画像'),
        upload_to='questions',
        blank=True,
    )
    answer_img = models.ImageField(
        _('回答画像'),
        upload_to='answers',
        blank=True,
    )

    def __str__(self):
        return self.content

class NamePlateList(models.Model):
    id = models.AutoField(primary_key=True)
    # 所持しているユーザ
    belong_user = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE)
    # 手札となる社員の社員番号
    emp_number = models.CharField(
        _('手札番号'),
        max_length=6
    )