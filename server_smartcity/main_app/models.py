from django.db import models
from usermanagement_24782014.models import CustomUser


class Report(models.Model):

    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('REPORTED', 'Reported'),
        ('VERIFIED', 'Verified'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DRAFT'
    )

    reporter = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Peta transisi status resmi: hanya boleh naik satu tahap, tidak boleh loncat.
    STATUS_TRANSITIONS = {
        'DRAFT': ['REPORTED'],
        'REPORTED': ['VERIFIED'],
        'VERIFIED': ['IN_PROGRESS'],
        'IN_PROGRESS': ['RESOLVED'],
        'RESOLVED': [],
    }

    def get_valid_next_statuses(self):
        return self.STATUS_TRANSITIONS.get(self.status, [])

    def __str__(self):
        return self.title
    
