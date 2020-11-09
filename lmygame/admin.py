from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee, Choice, Question

# Register your models here.
admin.site.register(Employee, UserAdmin)

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['content']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
