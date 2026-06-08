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
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # One checklist per user per visa type
        unique_together = ['user', 'visa_type']

    def __str__(self):
        return f"{self.user.email} — {self.visa_type}"

    @property
    def completion_percentage(self):
        items = self.items.all()
        if not items.exists():
            return 0
        completed = items.filter(is_done=True).count()
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
