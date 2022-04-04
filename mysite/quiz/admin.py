from django.contrib import admin

from .models import Label, Userr, Question, Option, Quiz, Result

admin.site.register(Label)
admin.site.register(Userr)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(Result)

class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'correct', 'question')

admin.site.register(Option, OptionAdmin)
