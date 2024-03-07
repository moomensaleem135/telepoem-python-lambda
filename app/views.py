from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import pandas as pd
from .utils import (
    TableProcessor,
    TableName,
    PoetTableProcessor,
    PoemTableProcessor,
    PoemCollectionTableProcessor,
    BoothTableProcessor,
    Handler,
)


class IndexView(GenericAPIView):

    def post(self, request):
        file = request.FILES["file"]
        try:
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
            return Response({"success": "Data saved successfully"})
        except Exception as e:
            return Response({"error": e})
