import pandas as pd
from enum import Enum
import math
from .models import (
    PhoneType,
    PoemType,
    PoemTopic,
    Poem,
    PoemCollection,
    PoemCollectionAndPoem,
    Poet,
    PoetAndPoem,
    Booth,
    BoothAndPoemCollection,
    BoothLoggingHistory,
    BoothMaintainer,
    TelepoemBoothType,
    SpecialTag,
    Language,
    DirectoryType,
    Era,
)


class TableProcessor:
    def __init__(self, df):
        self.df = df
        self.table_info_list = self.extract_table_info()

    def extract_table_info(self):
        tables_info = []
        for i, column in enumerate(self.df.columns):
            if "Unnamed:" in column:
                continue

            not_null_values = self.df[column].notnull().any()
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

    def extract_data_rows(self):
        columns = None
        data = []
        for _, row in self.df.iterrows():
            if not row.isnull().values.all() and len(row.values) > 0:
                if columns is None:
                    columns = row.values
                else:
                    data.append(row.values)
        return columns, data

    def create_table_dataframe(self, table_info):
        columns, data = self.extract_data_rows()
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

    def get_table_dataframes(self):
        return {
            tb_info["table_name"]: self.create_table_dataframe(tb_info)
            for tb_info in self.table_info_list
        }


class TableName(Enum):
    POET_INFORMATION = "POET INFORMATION"
    POEM_INFORMATION = "POEM INFORMATION"
    BOOTH_INFORMATION = "BOOTH INFORMATION"
    POEM_COLLECTION_INFORMATION = "PoemCollection Information"


class PoetTableProcessor(TableProcessor):
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


class PoemTableProcessor(TableProcessor):
    def populate_poem_table_according_to_db(table_df):
        column_mapping = {
            "status": "active",
            "era": "poemEra",
            "types": "poemTypes",
            "specialTags": "poemSpecialTags",
            "topics": "poemTopics",
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
        table_df["isAdultPoem"] = table_df["isAdultPoem"].map(
            {"YES": True, "NO": False}
        )
        return table_df


class PoemCollectionTableProcessor(TableProcessor):
    def populate_poemcollection_table_according_to_db(table_df):
        column_mapping = {
            "description": "poemCollectionDescription",
        }
        table_df = table_df.rename(columns=column_mapping)
        return table_df


class BoothTableProcessor(TableProcessor):
    def populate_booth_table_according_to_db(table_df):
        column_mapping = {
            "boothNumber": "number",
            "boothMaintainerName": "boothMaintainer",
            "address": "physicalAddress",
            "isAdaAccessible": "isADAAccessible",
        }
        table_df = table_df.rename(columns=column_mapping)
        table_df["active"] = table_df["active"].map({"YES": True, "NO": False})
        table_df["isADAAccessible"] = table_df["isADAAccessible"].map(
            {"YES": True, "NO": False}
        )
        return table_df


class Handler:
    def __init__(self, table_dfs):
        self.table_dfs = table_dfs

    def poets_handler(self):
        if self.table_dfs is None:
            return []
        try:
            poet_objs = []
            for index, poet in self.table_dfs.iterrows():
                existing_poet = Poet.objects.filter(
                    legalFirstName=poet.legalFirstName,
                    legalLastName=poet.legalLastName,
                )
                if existing_poet.exists():
                    existing_poet = existing_poet.first()
                    if poet.address:
                        existing_poet.address = poet.address
                    if poet.poetBiography:
                        existing_poet.poetBiography = poet.poetBiography
                    if poet.creditedFirstName:
                        existing_poet.creditedFirstName = poet.creditedFirstName
                    if poet.creditedLastName:
                        existing_poet.creditedLastName = poet.creditedLastName
                    if poet.email:
                        existing_poet.email = poet.email
                    if poet.state:
                        existing_poet.state = poet.state
                    if poet.status:
                        existing_poet.status = poet.status
                    if poet.city:
                        existing_poet.city = poet.city
                    if poet.isLaureate:
                        existing_poet.isLaureate = poet.isLaureate
                    if poet.phoneNum:
                        existing_poet.phoneNum = poet.phoneNum
                    if poet.photoCredit:
                        existing_poet.photoCredit = poet.photoCredit
                    if poet.website:
                        existing_poet.website = poet.website
                    if poet.zipCode:
                        existing_poet.zipCode = poet.zipCode
                    existing_poet.save()
                    print("Poet Updated")
                else:
                    existing_poet = Poet.objects.create(**poet)
                    print("Poet Created")
                poet_objs.append(existing_poet)
            return poet_objs
        except Exception as e:
            print(f"Error: {e}")

    def poems_handler(self):
        if self.table_dfs is None:
            return
        try:
            poem_objs = []
            for index, poem in self.table_dfs.iterrows():
                era = Era.objects.filter(name=poem["poemEra"]).first()
                if not era:
                    era = Era.objects.create(name=poem["poemEra"])
                poem["poemEra"] = era
                if poem["poemTypes"]:
                    types_split = poem["poemTypes"].split(", ")
                    poem_type_objects = [
                        PoemType.objects.get_or_create(name=name)[0]
                        for name in types_split
                    ]
                    # Maximum 2 types allowed
                    if len(poem_type_objects) > 2:
                        poem_type_objects = poem_type_objects[:2]
                    poem["poemTypes"] = ", ".join(
                        str(poem_type.id) for poem_type in poem_type_objects
                    )

                if poem["poemTopics"]:
                    topics_split = poem["poemTopics"].split(", ")
                    poem_topic_objects = [
                        PoemTopic.objects.get_or_create(name=name)[0]
                        for name in topics_split
                    ]
                    # Maximum 3 topics allowed
                    if len(poem_topic_objects) > 3:
                        poem_topic_objects = poem_topic_objects[:3]
                    poem["poemTopics"] = ", ".join(
                        str(poem_topic.id) for poem_topic in poem_topic_objects
                    )
                if poem["poemSpecialTags"]:
                    tags_split = poem["poemSpecialTags"].split(", ")
                    special_tag_objects = [
                        SpecialTag.objects.get_or_create(name=name)[0]
                        for name in tags_split
                    ]
                    poem["poemSpecialTags"] = ", ".join(
                        str(special_tag.id) for special_tag in special_tag_objects
                    )
                if poem["language"]:
                    languages_split = poem["language"].split(", ")
                    language_objects = [
                        Language.objects.get_or_create(name=name)[0]
                        for name in languages_split
                    ]
                    poem["language"] = ", ".join(
                        str(language.id) for language in language_objects
                    )
                poem_obj = Poem.objects.filter(
                    title=poem["title"],
                    poetId=poem["poetId"],
                ).first()
                if poem_obj:
                    poem_obj.producerName = poem["producerName"]
                    poem_obj.narratorName = poem["narratorName"]
                    poem_obj.recordingDate = poem["recordingDate"]
                    poem_obj.recordingSource = poem["recordingSource"]
                    poem_obj.poemEra = poem["poemEra"]
                    poem_obj.poemTypes = poem["poemTypes"]
                    poem_obj.poemTopics = poem["poemTopics"]
                    poem_obj.poemSpecialTags = poem["poemSpecialTags"]
                    poem_obj.language = poem["language"]
                    poem_obj.active = poem["active"]
                    poem_obj.optionalLegal = poem["optionalLegal"]
                    poem_obj.isChildrenPoem = poem["isChildrenPoem"]
                    poem_obj.isAdultPoem = poem["isAdultPoem"]
                    poem_obj.recordingDuration = poem["recordingDuration"]
                    poem_obj.telepoemNumber = poem["telepoemNumber"]
                    poem_obj.copyRights = poem["copyRights"]
                    poem_obj.poemText = poem["poemText"]
                    poem_obj.save()
                    print("Poem Updated")
                else:
                    poem_obj = Poem.objects.create(
                        **poem,
                    )
                    print("Poem Created")
                poet_and_poem_obj = PoetAndPoem.objects.filter(
                    poemId=poem_obj, poetId=poem["poetId"]
                ).first()
                if not poet_and_poem_obj:
                    PoetAndPoem.objects.create(poemId=poem_obj, poetId=poem["poetId"])
                    print("PoetAndPoem Created")
                poem_objs.append(poem_obj)
            return poem_objs
        except Exception as e:
            print(f"Error: {e}")

    def booths_handler(self):
        if self.table_dfs is None:
            return
        try:
            booth_objs_list = []
            for index, booth in self.table_dfs.iterrows():
                booth_objs = []
                booth_names = booth["boothName"].split("; ")
                booth_numbers = str(booth["number"]).split("; ")
                phone_types = booth["phoneType"].split("; ")
                booth_types = booth["boothType"].split("; ")

                # Check if the number of values in each column matches
                num_booths = max(
                    len(booth_names),
                    len(booth_numbers),
                    len(phone_types),
                    len(booth_types),
                )

                for i in range(num_booths):
                    booth_name = (
                        booth_names[i] if i < len(booth_names) else booth_names[-1]
                    )
                    booth_number = (
                        booth_numbers[i]
                        if i < len(booth_numbers)
                        else booth_numbers[-1]
                    )
                    phone_type = (
                        phone_types[i] if i < len(phone_types) else phone_types[-1]
                    )
                    booth_type = (
                        booth_types[i] if i < len(booth_types) else booth_types[-1]
                    )

                    phone_type_obj = PhoneType.objects.filter(name=phone_type).first()
                    if not phone_type_obj:
                        phone_type_obj = PhoneType.objects.create(name=phone_type)
                        print("PhoneType Created")

                    telepoem_booth_type_obj = TelepoemBoothType.objects.filter(
                        name=booth_type
                    ).first()
                    if not telepoem_booth_type_obj:
                        telepoem_booth_type_obj = TelepoemBoothType.objects.create(
                            name=booth_type
                        )
                        print("TelepoemBoothType Created")

                    directoryType_obj = DirectoryType.objects.filter(
                        name=booth["directoryType"]
                    ).first()
                    if not directoryType_obj:
                        directoryType_obj = DirectoryType.objects.create(
                            name=booth["directoryType"]
                        )
                        print("DirectoryType Created")

                    booth_maintainer = BoothMaintainer.objects.filter(
                        name=booth["boothMaintainer"]
                    ).first()
                    if not booth_maintainer:
                        booth_maintainer = BoothMaintainer.objects.create(
                            name=booth["boothMaintainer"]
                        )
                        print("BoothMaintainer Created")

                    # Create Booth object with the extracted values
                    booth_obj = Booth.objects.filter(boothName=booth_name).first()
                    if booth["zipCode"] == "":
                        booth["zipCode"] = None
                    if booth_obj:
                        booth_obj.number = booth_number
                        booth_obj.phoneType = phone_type_obj
                        booth_obj.boothType = telepoem_booth_type_obj
                        booth_obj.directoryType = directoryType_obj
                        booth_obj.boothMaintainer = booth_maintainer
                        booth_obj.directoryTabletSerialNumber = booth[
                            "directoryTabletSerialNumber"
                        ]
                        booth_obj.physicalAddress = booth["physicalAddress"]
                        booth_obj.city = booth["city"]
                        booth_obj.state = booth["state"]
                        booth_obj.zipCode = booth["zipCode"]
                        booth_obj.installationDate = booth["installationDate"]
                        booth_obj.installationType = booth["installationType"]
                        booth_obj.active = booth["active"]
                        booth_obj.isADAAccessible = booth["isADAAccessible"]
                        booth_obj.phoneSerialNumber = booth["phoneSerialNumber"]
                        booth_obj.installationNotes = booth["installationNotes"]
                        booth_obj.deviceInfo = booth["deviceInfo"]
                        booth_obj.save()
                        print("Booth Updated")
                    else:
                        booth_obj = Booth.objects.create(
                            boothName=booth_name,
                            number=booth_number,
                            phoneType=phone_type_obj,
                            boothType=telepoem_booth_type_obj,
                            directoryType=directoryType_obj,
                            boothMaintainer=booth_maintainer,
                            directoryTabletSerialNumber=booth[
                                "directoryTabletSerialNumber"
                            ],
                            physicalAddress=booth["physicalAddress"],
                            city=booth["city"],
                            state=booth["state"],
                            zipCode=booth["zipCode"],
                            installationDate=booth["installationDate"],
                            installationType=booth["installationType"],
                            active=booth["active"],
                            isADAAccessible=booth["isADAAccessible"],
                            phoneSerialNumber=booth["phoneSerialNumber"],
                            installationNotes=booth["installationNotes"],
                            deviceInfo=booth["deviceInfo"],
                        )
                        print("Booth Created")
                    booth_objs.append(booth_obj)
                booth_objs_list.append(booth_objs)
            return booth_objs_list
        except Exception as e:
            print(f"Error: {e}")

    def poem_collections_handler(self):
        if self.table_dfs is None:
            return
        try:
            for index, poemcollection in self.table_dfs.iterrows():
                poem_collection_obj = PoemCollection.objects.filter(
                    poemCollectionName=poemcollection["poemCollectionName"],
                ).first()
                if poem_collection_obj:
                    poem_collection_obj.poemCollectionName = (
                        poemcollection["poemCollectionName"],
                    )
                    poem_collection_obj.poemCollectionDescription = poemcollection[
                        "poemCollectionDescription"
                    ]
                    poem_collection_obj.save()
                    print("Poem Collection updated")
                else:
                    poem_collection_obj = PoemCollection.objects.create(
                        poemCollectionName=poemcollection["poemCollectionName"],
                        poemCollectionDescription=poemcollection[
                            "poemCollectionDescription"
                        ],
                    )
                    print("Poem Collection created")
                poem_collection_and_poem_obj = PoemCollectionAndPoem.objects.filter(
                    poemCollectionId=poem_collection_obj,
                    poemId=poemcollection["poemId"],
                ).first()
                if not poem_collection_and_poem_obj:
                    PoemCollectionAndPoem.objects.create(
                        poemCollectionId=poem_collection_obj,
                        poemId=poemcollection["poemId"],
                    )
                    print("Poem Collection and Poem created")
                for booth in poemcollection["boothId"]:
                    booth_and_poem_collection_obj = (
                        BoothAndPoemCollection.objects.filter(
                            booth=booth,
                            poemCollection=poem_collection_obj,
                        ).first()
                    )
                    if not booth_and_poem_collection_obj:
                        BoothAndPoemCollection.objects.create(
                            booth=booth,
                            poemCollection=poem_collection_obj,
                        )
                        print(f"Booth and Peom Collection created")
        except Exception as e:
            print(f"Error: {e}")
