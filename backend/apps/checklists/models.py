from django.db import models
from django.conf import settings
from apps.visas.models import VisaType, DocumentRequirement


class UserChecklist(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='checklists')
    visa_type = models.ForeignKey(VisaType, on_delete=models.CASCADE, related_name='user_checklists')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    target_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # One checklist per user per visa type
        unique_together = ['user', 'visa_type']

    def __str__(self):
        return f"{self.user.email} — {self.visa_type}"

    def sync_status(self):
        total = self.items.count()
        completed = self.items.filter(status='have_it').count()
        if total == 0:
            return
        if completed == total and self.status != 'completed':
            self.status = 'completed'
            self.save(update_fields=['status'])
        elif completed < total and self.status == 'completed':
            self.status = 'in_progress'
            self.save(update_fields=['status'])

    @property
    def completion_percentage(self):
        if 'completion_percentage' in self.__dict__ and self.__dict__['completion_percentage'] is not None:
            return round(self.__dict__['completion_percentage'])
        items = self.items.all()
        if not items.exists():
            return 0
        completed = items.filter(status='have_it').count()
        return round((completed / items.count()) * 100)


class ChecklistItem(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Not Yet'),
        ('have_it', 'I Have It'),
    ]

    checklist = models.ForeignKey(UserChecklist, on_delete=models.CASCADE, related_name='items')
    document = models.ForeignKey(DocumentRequirement, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    user_note = models.CharField(max_length=255, blank=True)  # optional personal reminder
    marked_done_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['checklist', 'document']

    @property
    def is_done(self):
        return self.status == 'have_it'
