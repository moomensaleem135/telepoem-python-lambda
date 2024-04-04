# File: myapp/management/commands/add_links.py
from django.core.management.base import BaseCommand
from app.models import Poem
from app.utils import S3


class Command(BaseCommand):
    help = "Run the process"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting the process..."))
        # Call your add_links method or include the logic here
        result = add_links()
        self.stdout.write(
            self.style.SUCCESS(f"Process completed with result: {result}")
        )


def add_links():
    try:
        print("Getting mp3 files from s3")
        bucket_name = "dataimportcsv"
        links = S3(bucket_name).get_audio_links()
        poem_objs = Poem.objects.all()
        print("Poems found: ", poem_objs.count())
        for poem in poem_objs:
            if poem.telepoemNumber:
                file_key = f"Poem recordings/{poem.telepoemNumber}.mp3"
                for link in links:
                    if link == file_key:
                        poem.audioLink = (
                            f"https://{bucket_name}.s3.amazonaws.com/{link}"
                        )
                        poem.save()
                        print("Poem updated")
                        break
    except Exception as e:
        raise e
    return "Process completed successfully"
