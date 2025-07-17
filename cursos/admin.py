from django.contrib import admin
from .models import Cursos, Module, Aula, Comentario

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'ordem')
    list_filter = ('curso',)
    ordering = ('curso', 'ordem')

class AulaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'modulo', 'video_id')
    fields = ('titulo', 'descricao', 'modulo', 'video_id')
    readonly_fields = []
    
    # Registrar o Aula com o admin personalizado
admin.site.register(Aula, AulaAdmin)

# Registrar os outros modelos simples
admin.site.register(Cursos)
admin.site.register(Comentario)
#admin.site.register(FAQ)
#admin.site.register(Quiz)
#admin.site.register(Pergunta)
#dmin.site.register(Alternativa)