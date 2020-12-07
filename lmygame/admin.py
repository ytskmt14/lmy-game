from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee, Question, NamePlateList

# Register your models here.
admin.site.register(Employee, UserAdmin)

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

admin.site.register(NamePlateList)
