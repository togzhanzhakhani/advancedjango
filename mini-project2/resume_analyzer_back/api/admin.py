from django.contrib import admin
from .models import Specialization, Skill, Resume

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1

class SpecialtyAdmin(admin.ModelAdmin):
    inlines = [SkillInline]

class ResumeAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'created_at']
    search_fields = ['user__username', 'specialization__name']

admin.site.register(Specialization, SpecialtyAdmin)
admin.site.register(Skill)
admin.site.register(Resume, ResumeAdmin)
