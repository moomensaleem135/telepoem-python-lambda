import pandas as pd
from enum import Enum
from tabulate import tabulate


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
    table_df[['legalLastName', 'legalFirstName']] = table_df['Legal Name'].str.split(', ', n=1, expand=True)
    table_df[["creditedLastName", "creditedFirstName"]] = table_df['Credited Name'].str.split(' and ', n=1, expand=True)

    column_mapping = {
        'Website': 'website',
        'Address': 'address',
        'Email': 'email',
        'Phone Number': 'phoneNum',
        'City': 'city',
        'Status': 'status',
        'Zip': 'zipCode',
        'Is Laureate': 'isLaureate',
        'Pic Credits': 'photoCredit',
        'State': 'state',
        'Poet Biography': 'poetBiography',
    }
    table_df = table_df.rename(columns=column_mapping)

    columns_to_remove = ['Legal Name', 'Credited Name', 'Additional Poets Name']
    table_df = table_df.drop(columns=columns_to_remove, errors='ignore')
    table_df['isLaureate'] = table_df['isLaureate'].map({'yes': True, 'no': False})
    return table_df


def populate_poem_table_according_to_db(table_df):
    column_mapping = {
        'Title': 'title',
        'Recording Duration': 'recordingDuration',
        'RecordingDate': 'recordingDate',
        'Recording Source': 'recordingSource',
        'Telepoem Number': 'telepoemNumber',
        'Copy Rights': 'copyRights',
        'Optional Legal': 'optionalLegal',
        'Producer Name': 'producerName',
        'Narrator Name': 'narratorName',
        'Topics': 'poemTopics',
        'Types': 'poemTypes',
        'Special Tags': 'poemSpecialTags',
        'Era': 'poemEra',
        'Poem Text': 'poemText',
        'Is Adult Poem': 'isAdultPoem',
        'Is Children Poem': 'isChildrensPoem',
        'Language': 'language',
        'Status': 'active',
    }
    table_df = table_df.rename(columns=column_mapping)

    columns_to_remove = ['Telepoem File Name']
    table_df = table_df.drop(columns=columns_to_remove, errors='ignore')
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
            print(tabulate(table_df, headers='keys', tablefmt='psql'))
            print("\n")


def print_df(table_df, table_name):
    print(f"{table_name} DataFrame:")
    print(tabulate(table_df, headers='keys', tablefmt='psql'))
    print("\n")

