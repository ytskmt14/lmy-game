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



