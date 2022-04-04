from django.contrib import admin

from .models import Rotulo, Usuario, Questao, Alternativa, Simulado, Resultado

admin.site.register(Rotulo)
admin.site.register(Usuario)
admin.site.register(Questao)
admin.site.register(Simulado)
admin.site.register(Resultado)

class AlternativaAdmin(admin.ModelAdmin):
    list_display = ('id', 'texto', 'correta', 'questao')

admin.site.register(Alternativa, AlternativaAdmin)