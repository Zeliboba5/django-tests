from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from tests.models import *
from nested_inline.admin import NestedStackedInline, NestedModelAdmin


class AnswerInlineFormSet(BaseInlineFormSet):
    def clean(self):
        count = 0
        right_count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
                    if form.cleaned_data['is_right']:
                        right_count += 1
            except AttributeError:
                pass
        if count == 0:
            return
        if count == 1:
            raise ValidationError('Вопрос должен иметь по крайней мере два ответа')
        elif right_count == count:
            raise ValidationError('Все ответы на вопрос не могут быть правльными')
        elif right_count == 0:
            raise ValidationError('Должен быть хотя бы один правильный ответ')


class QuestionInlineFormSet(BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
            except AttributeError:
                pass
        if count < 1:
            raise ValidationError('Должен быть по крайней мере один вопрос')


class AnswerInline(NestedStackedInline):
    model = Answer
    formset = AnswerInlineFormSet


class QuestionInline(NestedStackedInline):
    model = Question
    formset = QuestionInlineFormSet
    inlines = [AnswerInline]


class TestAdmin(NestedModelAdmin):
    model = Test
    inlines = [QuestionInline]


admin.site.register(Test, TestAdmin)
