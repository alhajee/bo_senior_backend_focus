import csv

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from repertoire.models import Contributor, File, Work


class Command(BaseCommand):
    help = "Deletes all data from the Contributor, Work, & File models"

    def handle(self, *args, **options):

         # clean database
        Contributor.objects.all().delete()
        Work.objects.all().delete()
        File.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully cleaned the Contributor, Work, & File models"
            )
        )