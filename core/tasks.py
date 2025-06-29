from celery import shared_task
from django.utils import timezone
from .models import Notification, Estagio

@shared_task
def send_deadline_alerts():
    now = timezone.now()
    soon = now + timezone.timedelta(days=3)
    estagios = Estagio.objects.filter(data_fim__range=(now, soon), status='EM_ANDAMENTO')
    for estagio in estagios:
        Notification.objects.get_or_create(
            user=estagio.estagiario.user,
            message=f"Seu estágio termina em breve: {estagio.data_fim}",
            due_date=estagio.data_fim,
            read=False,
        )