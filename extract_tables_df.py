import pandas as pd
from enum import Enum


def extract_table_info(df):
    tables_info = []
    for i, column in enumerate(df.columns):
        if "Unnamed:" in column:
            continue

        not_null_values = df[column].notnull().any()
        if not_null_values:
            if tables_info and "ending_index" not in tables_info[-1]:
                tables_info[-1]["ending_index"] = i

            tables_info.append(
                {
                    "table_name": column,
                    "starting_index": i,
                }
            )

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
    table_data = [
        index[table_info["starting_index"] : table_info["ending_index"]]
        for index in data
    ]
    table_df = pd.DataFrame(
        table_data,
        columns=columns[table_info["starting_index"] : table_info["ending_index"]],
    )
    if "tableSeperator" in table_df.columns:
        table_df = table_df.drop(columns="tableSeperator")
    table_df = table_df.fillna("")
    if table_df.empty:
        return None
    else:
        return table_df


class TableName(Enum):
    POET_INFORMATION = "POET INFORMATION"
    POEM_INFORMATION = "POEM INFORMATION"
    BOOTH_INFORMATION = "BOOTH INFORMATION"
    POEM_COLLECTION_INFORMATION = "PoemCollection Information"


def get_table_dataframes(file_path):
    df = pd.read_excel(file_path)
    table_info_list = extract_table_info(df)

    return {
        tb_info["table_name"]: create_table_dataframe(df, tb_info)
        for tb_info in table_info_list
    }


def populate_poet_table_according_to_db(table_df):
    table_df["legalLastName"], table_df["legalFirstName"] = zip(
        *table_df["legalName"].apply(
            lambda x: (
                ["", x.replace("(Unknown), ", "")]
                if "(Unknown)" in x
                else x.split(", ", 1)
            )
        )
    )

    table_df["creditedLastName"], table_df["creditedFirstName"] = zip(
        *table_df["creditedName"].apply(
            lambda x: (x.split(", ", 1) if len(x.split(", ")) > 1 else ["", x])
        )
    )
    table_df["status"] = table_df["status"].map(
        {"ACTIVE": True, "INACTIVE": False, "": False}
    )
    table_df["isLaureate"] = table_df["isLaureate"].map(
        {"YES": True, "NO": False, "": False}
    )
    column_mapping = {
        "phoneNumber": "phoneNum",
        "zip": "zipCode",
        "picCredits": "photoCredit",
    }
    table_df = table_df.rename(columns=column_mapping)

    columns_to_remove = ["legalName", "creditedName", "additionalPoetsName"]
    table_df = table_df.drop(columns=columns_to_remove, errors="ignore")
    return table_df


def populate_poem_table_according_to_db(table_df):
    column_mapping = {
        "status": "active",
    }
    table_df = table_df.rename(columns=column_mapping)
    columns_to_remove = [
        "Telepoem File Name",
        "telepoemPublicationCollection(Poem Collection)",
    ]
    table_df = table_df.drop(columns=columns_to_remove, errors="ignore")
    table_df["active"] = table_df["active"].map({"Active": True, "Inactive": False})
    table_df["recordingDate"] = (
        table_df["recordingDate"]
        .fillna(pd.NaT)
        .astype(object)
        .where(pd.notnull(table_df["recordingDate"]), None)
    )
    table_df["isChildrenPoem"] = table_df["isChildrenPoem"].map(
        {"YES": True, "NO": False}
    )
    table_df["isAdultPoem"] = table_df["isAdultPoem"].map({"YES": True, "NO": False})
    return table_df


def populate_tables_for_the_db(table_dfs):
    for table_name, table_df in table_dfs.items():
        if table_name == TableName.POET_INFORMATION.value:
            poet_df = populate_poet_table_according_to_db(table_df)
            # print_df(poet_df, table_name)
        elif table_name == TableName.POEM_INFORMATION.value:
            poem_df = populate_poem_table_according_to_db(table_df)
            print_df(poem_df, table_name)


def print_table_dfs(table_dfs):
    for table_name, table_df in table_dfs.items():
        if table_name == TableName.POET_INFORMATION.value:
            print(f"{table_name} DataFrame:")
            print("\n")


def print_df(table_df, table_name):
    print(f"{table_name} DataFrame:")
    print("\n")
