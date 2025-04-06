from django.db import models
from simple_history.models import HistoricalRecords

class Candidate(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    resume = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name = 'Кандидат'
        verbose_name_plural = 'Кандидаты'

class Interview(models.Model):
    STATUS_CHOICES = [
        ('запланировано', 'Запланировано'),
        ('проведено', 'Проведено'),
        ('отменено', 'Отменено'),
    ]

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='запланировано')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.candidate.name} — {self.date.strftime("%d.%m.%Y %H:%M")} ({self.status})'
    
    class Meta:
        verbose_name = 'Собеседование'
        verbose_name_plural = 'Собеседования'