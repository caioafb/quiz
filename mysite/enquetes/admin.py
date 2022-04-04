from django.contrib import admin
from .models import Pergunta, Opcao, Autor, Rotulo

class OpcaoInline(admin.TabularInline):
    model = Opcao
    extra = 2

class PerguntaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['autor', 'texto']}),
        ('Rótulo', {'fields':['rotulos']}),
        ('Informações de Data', {'fields': ['data_publicacao']}),
    ]
    inlines = [OpcaoInline]
    list_display = ('texto', 'id', 'autor', 'publicada_recentemente')
    list_filter = ['data_publicacao']
    search_fields = ['texto']

class AutorAdmin(admin.ModelAdmin):
    list_display = ('nome','id', 'genero', 'descricao')
    search_fields = ['nome']

class RotuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'id')

admin.site.register(Pergunta, PerguntaAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Rotulo, RotuloAdmin)
#admin.site.register(Opcao)
