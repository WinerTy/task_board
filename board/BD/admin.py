from django.contrib import admin

from .models import Post, Response, Email

# Register your models here.



class EmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sent')


admin.site.register(Post)
admin.site.register(Response)
admin.site.register(Email, EmailAdmin)