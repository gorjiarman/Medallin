from django.contrib import admin

from api import models


class TokenAdmin(admin.ModelAdmin):
    list_display = ('label', 'token', 'expires')
    list_filter = ('expires', )


admin.site.register(models.Token, TokenAdmin)
