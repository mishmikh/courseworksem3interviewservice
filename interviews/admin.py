from django.contrib import admin
from .models import Candidate, Interview
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ExportActionMixin


class InterviewInline(admin.TabularInline):
    model = Interview
    extra = 0


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']
    fields = ['name', 'email', 'phone', 'resume']
    inlines = [InterviewInline] 


@admin.register(Interview)
class InterviewAdmin(ExportActionMixin, SimpleHistoryAdmin):
    list_display = ['candidate_link', 'date', 'status']
    list_display_links = ['candidate_link']
    list_filter = ['status']
    fieldsets = (
        (None, {'fields': ('candidate', 'date', 'status')}),
        ('Дополнительно', {'fields': ('notes',)}),
    )

    def candidate_link(self, obj):
        return obj.candidate.name
    
    candidate_link.short_description = 'Кандидат'
    
    actions = ['cancel_old_interviews'] #добавил дополнительное действие с командой удаления истекших интервью

    @admin.action(description='Отменить устаревшие собеседования')
    def cancel_old_interviews(self, request, queryset):
        from django.utils import timezone
        now = timezone.now()
        old = queryset.filter(status='запланировано', date__lt=now)
        updated = old.update(status='отменено')
        self.message_user(request, f'Отменено {updated} собеседований.')
