# File: myapp/management/commands/run_process.py
import pandas as pd
from app.utils import (
    TableProcessor,
    TableName,
    PoetTableProcessor,
    PoemTableProcessor,
    PoemCollectionTableProcessor,
    BoothTableProcessor,
    Handler,
    get_excel_file,
)
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run the process"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting the process..."))
        # Call your run_process method or include the logic here
        result = run_process()
        self.stdout.write(
            self.style.SUCCESS(f"Process completed with result: {result}")
        )


def run_process():
    try:
        file_name = "file.xlsx"
        file = get_excel_file(file_name)
        df = pd.read_excel(file)
        table_dfs = TableProcessor(df).get_table_dataframes()
        poet_ids = []
        poem_ids = []
        booth_ids = []
        for table_name, table_df in table_dfs.items():
            if table_name == TableName.POET_INFORMATION.value:
                poet_df = PoetTableProcessor.populate_poet_table_according_to_db(
                    table_df
                )
                poet_ids = Handler(poet_df).poets_handler()
            elif table_name == TableName.POEM_INFORMATION.value:
                poem_df = PoemTableProcessor.populate_poem_table_according_to_db(
                    table_df
                )
                poem_df["poetId"] = poet_ids
                poem_ids = Handler(poem_df).poems_handler()
            elif table_name == TableName.BOOTH_INFORMATION.value:
                booth_df = BoothTableProcessor.populate_booth_table_according_to_db(
                    table_df
                )
                booth_ids = Handler(booth_df).booths_handler()
            elif table_name == TableName.POEM_COLLECTION_INFORMATION.value:
                poemcollection_df = PoemCollectionTableProcessor.populate_poemcollection_table_according_to_db(
                    table_df
                )
                poemcollection_df["poemId"] = poem_ids
                poemcollection_df["boothId"] = booth_ids
                Handler(poemcollection_df).poem_collections_handler()
    except Exception as e:
        raise e
    return "Process completed successfully"
