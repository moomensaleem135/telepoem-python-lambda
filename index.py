import os
from dotenv import load_dotenv
from database import initialize_session

load_dotenv()  # Load environment variables from .env file

from extract_tables_df import (
    get_table_dataframes,
    populate_tables_for_the_db,
    TableName,
    populate_poet_table_according_to_db,
    populate_poem_table_according_to_db,
    print_df,
)

# from s3_operations import read_excel_from_s3
from poet import poets_handler
from additional_tables import poems_handler

# from booth import booths_handler
from poem_collection import (
    poem_collections_handler,
)  # Import poem_collections_handler function
from sqlalchemy.exc import SQLAlchemyError

db_session = initialize_session()

def handler(event=None, args=None):
    try:
        FILE_PATH = "./xlx_files/file.xlsx"
        if not os.path.exists(FILE_PATH):
            raise ValueError("No file found in the specified path.")
        table_dfs = get_table_dataframes(FILE_PATH)
        poet_ids = []
        for table_name, table_df in table_dfs.items():
            if table_name == TableName.POET_INFORMATION.value:
                poet_df = populate_poet_table_according_to_db(table_df)
                print_df(poet_df, table_name)
                poet_ids = poets_handler(poet_df)
            elif table_name == TableName.POEM_INFORMATION.value:
                poem_df = populate_poem_table_according_to_db(table_df)
                print_df(poem_df, table_name)
                poem_df["poetId"] = poet_ids
                poems_handler(poems=poem_df)

        # excel_data = read_excel_from_s3("TelePoem data.xlsx")
        #
        # for sheet_name, df in excel_data.items():
        #     print(f"Sheet: {sheet_name}")
        #     if sheet_name == "Poet":
        #         print("=" * 50)
        #         poets_handler(df)
        #     elif sheet_name == "Booth":  # Check if sheet is Booth
        #         print("=" * 50)
        #         booths_handler(df)  # Call booths_handler function
        #     elif sheet_name == "Poem-Collection":  # Check if sheet is PoemCollection
        #         print("=" * 50)
        #         poem_collections_handler(df)
    except SQLAlchemyError as e:
        print("An SQLAlchemy error occurred:", e)
    except Exception as e:
        print("An error occurred:", e)


handler()
