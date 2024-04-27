"""
Django Command to wait for DB to be available
"""

import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2Error


class Command(BaseCommand):
    """Django Command to wait for DB"""

    def handle(self, *args, **options):
        """Entry point for command to wait for DB to be available"""
        self.stdout.write("Waiting for DB to be available...")

        db_up = False

        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (OperationalError, Psycopg2Error):
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
