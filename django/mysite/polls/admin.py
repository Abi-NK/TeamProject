from django.contrib import admin

# Register your models here.
from .models import Choice, Question

# css stcked inline
#class ChoiceInline(admin.StackedInline):
#    model = Choice
#    extra = 3

# Tabular inline css more compact
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    #fields = ['pub_date', 'question_text'] # fields not fieldsets
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    # list display for questions page, adds date published and published recent
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
# register Chioce for forms, removed for 
#admin.site.register(Choice)
