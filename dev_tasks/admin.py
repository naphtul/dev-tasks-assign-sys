from django.contrib import admin

from .models import Developer, Task, Team


class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('MainBranch', 'EdLevel', 'LanguageHaveWorkedWith', 'WebframeHaveWorkedWith', 'is_full',
                    'is_pro', 'is_academic', 'is_front', 'is_back')
    fields = ['team_id', 'MainBranch', 'EdLevel', 'LanguageHaveWorkedWith', 'WebframeHaveWorkedWith']


class TaskAdmin(admin.ModelAdmin):
    list_display = ('type', 'points', 'created', 'assigned')


admin.site.register(Developer, DeveloperAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Team)
