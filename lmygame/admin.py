from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee, Choice, Question, Answer

# Register your models here.
admin.site.register(Employee, UserAdmin)

def clear_all_is_selected(modeladmin, request, queryset):
    """
    選択済フラグをすべておろす
    """
    queryset.update(is_selected=False)

clear_all_is_selected.short_description = "選択済フラグを解除する"

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'is_selected')
    actions = [clear_all_is_selected]
    fieldsets = [
        (None, {'fields': ['content', 'is_selected']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                'respondent', 'answer', 'question'
            ),
        }),
    )

admin.site.register(Answer, AnswerAdmin)