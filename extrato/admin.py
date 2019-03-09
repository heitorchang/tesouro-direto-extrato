from django.contrib import admin

from .models import Tipo, Titulo, Corretora, Transacao

admin.site.register(Tipo)
admin.site.register(Titulo)
admin.site.register(Corretora)
admin.site.register(Transacao)

