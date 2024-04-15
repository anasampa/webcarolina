from django.contrib import admin
from .models import *

# Models admin painel registration
admin.site.register(Publicacao)
admin.site.register(Equipe, EquipeAdmin)
admin.site.register(Tema)
admin.site.register(Subtema, SubtemaAdmin)
admin.site.register(CarolinaVersao)
admin.site.register(Atributo,AtributoAdmin)
admin.site.register(Filtro,FiltroAdmin)
admin.site.register(TextoArmazenamento, TextoArmazenamentoAdmin)
admin.site.register(Text,TextAdmin)
