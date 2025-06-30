from celery import shared_task
from django.utils import timezone
from .models import Estagio, Notificacao

@shared_task
def send_deadline_alerts():
    hoje = timezone.now().date()
    limite = hoje + timezone.timedelta(days=3)
    estagios = Estagio.objects.filter(
        data_fim__range=(hoje, limite), status='EM_ANDAMENTO'
    )
    for estagio in estagios:
        Notificacao.objects.get_or_create(
            estagiario=estagio.estagiario,
            titulo='Prazo do Estágio',
            mensagem=f'Seu estágio termina em breve: {estagio.data_fim}',
            tipo='ALERTA',
        )