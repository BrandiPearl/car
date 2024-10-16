import json
from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Load data from project_dump.json into the database'

    def handle(self, *args, **kwargs):
        with open('project_dump.json', 'r') as file:
            data = json.load(file)
            for entry in data:
                model_name = entry.get('model')
                pk = entry.get('pk')
                fields = entry.get('fields')

                if not model_name or not pk or not fields:
                    self.stdout.write(self.style.ERROR(f'Missing data in entry: {entry}'))
                    continue

                model = apps.get_model(model_name)
                obj, created = model.objects.update_or_create(pk=pk, defaults=fields)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created {model_name} with pk {pk}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated {model_name} with pk {pk}'))