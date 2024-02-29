import pandas as pd


def extract_table_info(df):
    tables_info = []
    for i, column in enumerate(df.columns):
        if "Unnamed:" in column:
            continue

        not_null_values = df[column].notnull().any()
        if not_null_values:
            if tables_info and "ending_index" not in tables_info[-1]:
                tables_info[-1]["ending_index"] = i

            tables_info.append({
                "table_name": column,
                "starting_index": i,
            })

    if tables_info and "ending_index" not in tables_info[-1]:
        tables_info[-1]["ending_index"] = i + 1

    return tables_info


def extract_data_rows(df):
    columns = None
    data = []
    for _, row in df.iterrows():
        if not row.isnull().values.all() and len(row.values) > 0:
            if columns is None:
                columns = row.values
            else:
                data.append(row.values)
    return columns, data


def create_table_dataframe(df, table_info):
    columns, data = extract_data_rows(df)
    table_data = [index[table_info["starting_index"]:table_info["ending_index"]] for index in data]
    table_df = pd.DataFrame(table_data, columns=columns[table_info["starting_index"]:table_info["ending_index"]])
    return table_df.dropna()


def get_table_dataframes(file_path):
    df = pd.read_excel(file_path)
    table_info_list = extract_table_info(df)

    poet_info = poem_info = booth_info = poem_collection_info = None
    for tb_info in table_info_list:
        if tb_info["table_name"] == "POET INFORMATION":
            poet_info = tb_info
        elif tb_info["table_name"] == "POEM INFORMATION":
            poem_info = tb_info
        elif tb_info["table_name"] == "BOOTH INFORMATION":
            booth_info = tb_info
        elif tb_info["table_name"] == "PoemCollection Information":
            poem_collection_info = tb_info

    poet_df = create_table_dataframe(df, poet_info)
    poem_df = create_table_dataframe(df, poem_info)
    booth_df = create_table_dataframe(df, booth_info)
    poem_collection_df = create_table_dataframe(df, poem_collection_info)

    return poet_df, poem_df, booth_df, poem_collection_df
