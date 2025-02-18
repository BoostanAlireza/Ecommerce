from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import connection


class Command(BaseCommand):
    help = 'Truncate all tables in the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Truncating all tables...')
        truncate_all_tables()
        self.stdout.write('All tables truncated successfully.')


def truncate_all_tables():
    with connection.cursor() as cursor:
        cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
        for model in apps.get_models():
            table_name = model._meta.db_table
            cursor.execute(f'TRUNCATE TABLE `{table_name}`;')
        cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')
