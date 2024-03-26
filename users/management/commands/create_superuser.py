import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from dotenv import load_dotenv


class Command(BaseCommand):
    help = 'Create superuser if not exists'

    def handle(self, *args, **options):
        load_dotenv(override=True)
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                email=os.environ.get('SUPERUSER_EMAIL'),
                username=os.environ.get('SUPERUSER_USERNAME'),
                first_name=os.environ.get('SUPERUSER_FIRST_NAME'),
                last_name=os.environ.get('SUPERUSER_LAST_NAME'),
                password=os.environ.get('SUPERUSER_PASSWORD'),
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))
