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

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    content = models.TextField(
        _('問題文'),
    )
    is_selected = models.BooleanField(
        _('選択済'),
        default=False,
    )

    def __str__(self):
        return self.content

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(
        _('選択肢'),
        max_length=50,
    )
    is_correct = models.BooleanField(
        _('正解'),
        default=False
    )
