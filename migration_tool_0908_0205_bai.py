# 代码生成时间: 2025-09-08 02:05:09
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.utils import DEFAULT_DB_ALIAS

"""
A Django management command for performing database migrations.
This command is designed to handle database migrations in a Django application.
It follows Django's best practices for database operations.
"""

class Command(BaseCommand):
    help = 'Perform database migrations'

    def add_arguments(self, parser):
        """
        Add custom arguments to the command
        """
        parser.add_argument('--database', dest='database', default=DEFAULT_DB_ALIAS,
                        help='Nominates a database to migrate. Defaults to the "default" database.')
        parser.add_argument('--fake', action='store_true', dest='fake', default=False,
                        help='Fake migrate for the given database.')

    def handle(self, *args, **options):
        """
        Handle the command-line arguments and perform the database migration.
        """
        # Get the database alias from options
        database = options['database']
        
        # Get the fake migration flag from options
        fake = options['fake']
        
        # Perform the migration
        try:
            self.stdout.write(self.style.MIGRATE_HEADING('Running migrations...'))
            call_command('migrate', database=database, fake=fake)
            self.stdout.write(self.style.SUCCESS('Successfully performed migrations.'))
        except Exception as e:
            # Handle any migration exceptions
            self.stdout.write(self.style.ERROR('An error occurred during migration: %s' % e))
            raise
