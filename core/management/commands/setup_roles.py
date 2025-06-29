from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from core.models import User


class Command(BaseCommand):
    help = 'Cria grupos e permissões para roles do sistema'

    def handle(self, *args, **kwargs):
        roles = ['COORDENADOR', 'SUPERVISOR', 'ALUNO']
        for role in roles:
            group, created = Group.objects.get_or_create(name=role)
            self.stdout.write(self.style.SUCCESS(f'Grupo {role} {"criado" if created else "já existe"}'))
        # Adicione permissões específicas por grupo conforme necessário