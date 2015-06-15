from django.contrib import admin
from django.db.models import Count

from polls.models import Poll, Choice, Answer, Question



class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3

class PollAdmin(admin.ModelAdmin):
    list_display = ('key', 'published')
    list_filter  = ['published']
    search_fields = ['question']
    inlines = [QuestionInline]

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'question', 'answer_count')
    inlines = [AnswerInline]

    def queryset(self, request):
        super(ChoiceAdmin, self).queryset(request)
        return Choice.objects.annotate(total_answers=Count('answer'))

    def answer_count(self, obj):
        return obj.total_answers

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('created', 'choice')

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('label', 'poll')
    inlines = [ChoiceInline]

admin.site.register(Poll, PollAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)

