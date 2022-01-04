import csv
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from repertoire.models import Contributor, File, Work


class Command(BaseCommand):
    help = "Loads musical works from CSV file and saves them in database"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

        # # Named (optional) arguments
        parser.add_argument(
            '--header',
            help='Does csv file has headers',
            type=bool
        )

    def handle(self, *args, **options):
        start_time = timezone.now()
        file_path = options["file_path"]
        
        header = True

        # check if optional header argument was provided
        if options['header']:
            header = options['header']

        try:
            with open(file_path, "r") as csv_file:
                # does csv file has header

                # get start time
                start_time = timezone.now()
                
                # define the max rows to insert into the database
                MAX_ROWS = 1000

                # create a data reader
                data = csv.reader(csv_file, delimiter=",")

                # get number of rows in file
                row_count = sum(1 for row in data)

                # list to store object of musical works
                works = list()

                # save file metadata in model if file is not empty
                if row_count > 0:    
                    file = File(
                        filename = file_path,
                        work_count = row_count
                    )
                    file.save()
                else:
                    self.stderr.write(
                        'Empty file'
                    )
                    # raise exception if file is empty
                    raise CommandError('Cannot process file with 0 rows')

                # define default index of columns
                columns = {
                    "title": 0,
                    "contributors": 1,
                    "iswc": 2,
                    "source": 3,
                    "proprietary_id": 4
                }

                # read works and save them in database
                for row in data:

                    # run once and update column index if 
                    # headers do not come in expected order
                    if header:
                        for index, column_name in enumerate(row):
                            columns[column_name] = index
                        # set header to false to only execute this code once
                        header = False
                
                    # get the various name of contributors
                    contributor_list = row[columns.get("contributors")]
                    contributor_list = contributor_list.split("|")
                    # a list of contributor objects
                    contributors = list()

                    # create the contributors in the database
                    for contributor in contributor_list:
                        obj, created = Contributor.objects.get_or_create(
                            name=contributor
                        )
                        obj.save()
                        contributors.append(obj)

                    # create object from metadata on a musical work
                    work = Work(
                        title=row[columns.get("title")],
                        iswc=row[columns.get("iswc")],
                        source=row[columns.get("source")],
                        proprietary_id=row[columns.get("proprietary_id")]
                    )
                    
                    # add contributors
                    for contributor in contributors:
                        work.contributor.add(contributor)

                    # append musical works for bulk insertion
                    works.append(work)

                    # run a bulk insert once the number of works exceed MAX_ROWS
                    if len(works) > MAX_ROWS:
                        Work.objects.bulk_create(works)
                        works = []

                # run a bulk insert if number of works isn't up to MAX_ROWS
                if works:
                    Work.objects.bulk_create(works)

                end_time = timezone.now()
   
        except Exception as e:
            raise FileNotFoundError('File "%s" does not exist' % file_path)

        self.stdout.write(
            self.style.SUCCESS(
                f"Loading CSV took: {(end_time-start_time).total_seconds()} seconds."
            )
        )