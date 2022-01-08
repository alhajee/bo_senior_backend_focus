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
        # clean database
        Contributor.objects.all().delete()
        Work.objects.all().delete()
        File.objects.all().delete()

        start_time = timezone.now()
        file_path = options["file_path"]
        
        header = True

        # check if optional header argument was provided
        if options['header']:
            header = options['header']

        try:
            with open(f"/files/{file_path}", "r") as csv_file:
                # does csv file has header

                # get start time
                start_time = timezone.now()
                
                # define the max rows to insert into the database
                MAX_ROWS = 1000

                # define default index of columns
                columns = {
                    "title": 0,
                    "contributors": 1,
                    "iswc": 2,
                    "source": 3,
                    "proprietary_id": 4
                }

                # create a data reader
                csv_reader = csv.reader(csv_file, delimiter=",")

                # # get number of rows in file
                # row_count = sum(1 for row in csv_reader)
                row_count = 0
                
                header_list = list()

                # update column index if headers do not come in expected order
                if header is True:
                    header_list = next(csv_reader)

                    for index, column_name in enumerate(header_list):
                        columns[column_name] = index
                
                # list to store object of musical works
                works = list()
                contributor_ids = list()
                # save file metadata in model
                file = File(
                    filename = file_path,
                    work_count = row_count
                )
                file.save()
            
                # read works and save them in batches into database
                for row in csv_reader:
                    # get the various name of contributors
                    contributor_list = row[columns.get("contributors")]
                    contributor_list = contributor_list.split("|")

                    # create object from metadata on a musical work
                    work = Work(
                        file=file,
                        title=row[columns.get("title")],
                        iswc=row[columns.get("iswc")],
                        source=row[columns.get("source")],
                        proprietary_id=row[columns.get("proprietary_id")]
                    )

                    # save contributors or get ID if it exist in the database
                    temp_contributors = list()
                    for contributor in contributor_list:
                        obj, created = Contributor.objects.get_or_create(
                            name=contributor
                        )
                        # save if object was created not retrieved
                        if created:
                            # print(f"created {created}")
                            obj.save()

                        temp_contributors.append(obj.id)                        
                        # work.save()
                        # work.contributors.add(obj)
                    contributor_ids.append(set(temp_contributors))

                    # append musical works for bulk insertion
                    works.append(work)

                # run a bulk insert with a batch size of MAX_ROWS
                if works:
                    work_ids = Work.objects.bulk_create(works, batch_size=MAX_ROWS)

                    jobs = list()
                    for (work_id, contributor_id) in zip(work_ids, contributor_ids):
                        # print(work_id, contributor_id)
                        for id in contributor_id:
                           jobs.append(Work.contributors.through(contributor_id=id, work_id=work_id.id))
                    Work.contributors.through.objects.bulk_create(jobs)

                end_time = timezone.now()
   
        except FileNotFoundError as e:
            raise FileNotFoundError('File "%s" does not exist' % file_path)
        except Exception as e:
            print(e)

        self.stdout.write(
            self.style.SUCCESS(
                f"Loading CSV took: {(end_time-start_time).total_seconds()} seconds."
            )
        )