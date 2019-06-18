from django.contrib import admin
from .models import User, Feedback, ExtendedUser, Chat

admin.site.register(User)
admin.site.register(Feedback)
admin.site.register(Chat)

@admin.register(ExtendedUser)
class ExtendedUserAdmin(admin.ModelAdmin):
    readonly_fields = ('ava',)
