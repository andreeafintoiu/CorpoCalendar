from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Department,
    User,
    Manager,
    PersonalEvent,
    CompanyEvent,
    EventParticipation,
    SupportTicket,
)

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Date Angajat', {
            'fields': ('employee_id', 'department'),
        }),
    )
    list_display = ('username', 'email', 'employee_id', 'department', 'is_staff')
    list_filter = ('department', 'is_staff')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'assigned_at')
    list_filter = ('department',)

@admin.register(PersonalEvent)
class PersonalEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'start_time', 'end_time', 'location')
    list_filter = ('start_time',)

@admin.register(CompanyEvent)
class CompanyEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'department', 'start_time', 'end_time', 'location')
    list_filter = ('department', 'start_time')

@admin.register(EventParticipation)
class EventParticipationAdmin(admin.ModelAdmin):
    list_display = ('event', 'employee', 'status')
    list_filter = ('status',)

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'employee_id_entered', 'subject', 'is_resolved', 'created_at')
    list_editable = ('is_resolved',)
    list_filter = ('is_resolved',)

admin.site.register(User, CustomUserAdmin)
