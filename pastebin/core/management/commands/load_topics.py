from django.core.management.base import BaseCommand
from core.models import Topic

class Command(BaseCommand):
    help = 'Load initial topics'

    def handle(self, *args, **options):
        topics = [
            {'title': 'Python', 'description': 'Код на Python'},
            {'title': 'JavaScript', 'description': 'Скрипты и веб-разработка'},
            {'title': 'HTML/CSS', 'description': 'Верстка и стили'},
            {'title': 'Конфиги', 'description': 'Файлы конфигурации'},
            {'title': 'Текст', 'description': 'Произвольный текст'},
            {'title': 'Команды', 'description': 'Терминальные команды'},
            {'title': 'SQL', 'description': 'Запросы к базам данных'},
            {'title': 'Docker', 'description': 'Dockerfile и конфиги'},
        ]
        
        for topic_data in topics:
            topic, created = Topic.objects.get_or_create(
                title=topic_data['title'],
                defaults={'description': topic_data['description']}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created topic: {topic.title}')
                )