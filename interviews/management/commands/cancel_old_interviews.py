from django.core.management.base import BaseCommand
from interviews.models import Interview
from django.utils import timezone


class Command(BaseCommand):
    help = 'Cancels all interviews in the past that are still запланировано'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        old_interviews = Interview.objects.filter(status='запланировано', date__lt=now)
        count = old_interviews.count()
        old_interviews.update(status='отменено')
        self.stdout.write(self.style.SUCCESS(f'Cancelled {count} old interviews'))
