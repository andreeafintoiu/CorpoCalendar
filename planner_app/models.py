from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True) # Information Technologies, Human Resources, Sales
    code = models.CharField(max_length=20, unique=True) #D_IT, D_HR, D_SA

    def __str__(self):
        return f"{self.name} ({self.code})"

class User(AbstractUser):
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')

    def __str__(self):
        dept = self.department_name if self.department else "Fără departmanet"
        return f"{self.username} ({self.employee_id or 'Fără ID'} - {dept})"

class Manager(models.Model):
    """Leaga un utilizator cu rol de manager de departamentul pe care il conduce"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='managers')
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Manager: {self.user.get_full_name() or self.user.username} ({self.department.name})"

class PersonalEvent(models.Model):
    """Evenimentele personale ale unui angajat/manager"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='personal_events')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("Ora de sfârșit trebuie să fie după ora de început.")

    def __str__(self):
        return f"[Personal] {self.title} = {self.user.username} ({self.start_time.strftime('%d.%m %H:%M')})"

class CompanyEvent(models.Model):
    """Evenimente de companie, sedinte setate de manageri"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, help_text="Adresă fizică / Link Online")
    created_by = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='organized_events')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    def clean(self):
            if self.end_time <= self.start_time:
                raise ValidationError("Ora de sfârșit trebuie să fie după ora de început.")

    def __str__(self):
        return f"[Companie] {self.title} ({self.start_time.strftime('%d.%m %H:%M')})"

class EventParticipation(models.Model):
    """Evenimentele de companie la care participa un angajat (invitatii/tags)"""
    STATUS_CHOICES = [
        ('INVITED', 'Invitat'),
        ('CONFIRMED', 'Confirmat'),
        ('DECLINED', 'Respins'),
    ]
    event = models.ForeignKey(CompanyEvent, on_delete=models.CASCADE, related_name='participations')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_participations')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='CONFIRMED')

    class Meta:
        unique_together = ('event', 'employee')

    def __str__(self):
        return f"{self.employee.username} -> {self.event.title} ({self.get_status_display()})"

class SupportTicket(models.Model):
    """Tichete de suport pentru probleme la inregistrare (ID) sau in aplicatie"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    employee_id_entered = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    subject = models.CharField(max_length=150, default="Problemă ID angajat")
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tichet #{self.id} = {self.email} ({'Rezolvat' if self.is_resolved else 'Deschis'})"
    
