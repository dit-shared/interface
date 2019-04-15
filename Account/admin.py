from django.contrib import admin
from .models import User, Feedback, ExtendedUser

admin.site.register(User)
admin.site.register(Feedback)

@admin.register(ExtendedUser)
class ExtendedUserAdmin(admin.ModelAdmin):
    readonly_fields = ('ava',)
