from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Paste, Topic

class Command(BaseCommand):
    help = 'Удаляет просроченные пасты'

    def handle(self, *args, **options):
        # Находим просроченные пасты
        expired_pastes = Paste.objects.filter(expires_at__lte=timezone.now())
        count = expired_pastes.count()
        
        if count > 0:
            # Собираем темы, которые нужно обновить
            topics_to_update = set()
            for paste in expired_pastes:
                if paste.topic:
                    topics_to_update.add(paste.topic)
            
            # Выводим информацию о удаляемых пастах
            self.stdout.write(f'Найдено {count} просроченных паст:')
            for paste in expired_pastes:
                self.stdout.write(f' - {paste.title} (истек: {paste.expires_at})')
            
            # Удаляем пасты
            expired_pastes.delete()
            
            # Обновляем темы
            for topic in topics_to_update:
                topic.update_updated_at()
                self.stdout.write(f'Обновлена тема: {topic.title}')
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Успешно удалено {count} просроченных паст')
            )
        else:
            self.stdout.write('ℹ️ Просроченных паст не найдено')