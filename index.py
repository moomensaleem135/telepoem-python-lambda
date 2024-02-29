from dotenv import load_dotenv
from s3_operations import read_excel_from_s3
from poet import poets_handler
from booth import booths_handler
from poem_collection import poem_collections_handler  # Import poem_collections_handler function
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()  # Load environment variables from .env file


def handler(event=None, args=None):
    try:
        excel_data = read_excel_from_s3("TelePoem data.xlsx")

        for sheet_name, df in excel_data.items():
            print(f"Sheet: {sheet_name}")
            if sheet_name == "Poet":
                print("=" * 50)
                poets_handler(df)
            elif sheet_name == "Booth":  # Check if sheet is Booth
                print("=" * 50)
                booths_handler(df)  # Call booths_handler function
            elif sheet_name == "Poem-Collection":  # Check if sheet is PoemCollection
                print("=" * 50)
                poem_collections_handler(df)
    except SQLAlchemyError as e:
        print("An SQLAlchemy error occurred:", str(e))
    except Exception as e:
        print("An error occurred:", str(e))

handler()
