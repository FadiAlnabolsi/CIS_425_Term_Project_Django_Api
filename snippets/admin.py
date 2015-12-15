from django.contrib import admin
from snippets.models import Registrations, ScholarshipAdmin
# Register your models here.
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


admin.site.register(Registrations)

class Scholarship_Admin(admin.StackedInline):
	model = ScholarshipAdmin
	can_delete = False
	verbose_name_plural = 'Scholarship_Amdin'

class ScholarAdmin(UserAdmin):
	inlines = (Scholarship_Admin, )

admin.site.unregister(User)
admin.site.register(User, ScholarAdmin)
