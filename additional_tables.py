import uuid

from database import destroy_session, commit_and_destroy_session, initialize_session


def get_existing_era(db_session, era_name):
    from entities import Era
    return (
        db_session.query(Era)
        .filter(Era.name == era_name, )
        .first()
    )


def add_new_era(db_session, era_name):
    from entities import Era
    print("adding new era......")
    era = Era(name=era_name)
    db_session.add(era)


def get_existing_poem_topic(db_session, topic_name):
    from entities import PoemTopic
    return (
        db_session.query(PoemTopic)
        .filter(PoemTopic.name == topic_name, )
        .first()
    )


def add_new_poem_topic(db_session, topic_name):
    from entities import PoemTopic
    print("adding new poem_topic......")
    poem_topic = PoemTopic(name=topic_name)
    db_session.add(poem_topic)


def get_existing_poem_type(db_session, type_name):
    from entities import PoemType
    return (
        db_session.query(PoemType)
        .filter(PoemType.name == type_name, )
        .first()
    )


def add_new_poem_type(db_session, type_name):
    from entities import PoemType
    print("adding new poem_type......")
    poem_type = PoemType(name=type_name)
    db_session.add(poem_type)


def get_existing_poem_language(db_session, language_name):
    from entities import Language
    return (
        db_session.query(Language)
        .filter(Language.name == language_name, )
        .first()
    )


def add_new_poem_language(db_session, language_name):
    from entities import Language
    print("adding new poem_language......")
    poem_language = Language(name=language_name)
    db_session.add(poem_language)


def get_existing_special_tag(db_session, special_tag_name):
    from entities import SpecialTag
    return (
        db_session.query(SpecialTag)
        .filter(SpecialTag.name == special_tag_name, )
        .first()
    )


def add_new_special_tag(db_session, special_tag_name):
    from entities import SpecialTag
    print("adding new special_tag......")
    special_tag = SpecialTag(name=special_tag_name)
    db_session.add(special_tag)


def add_new_poem(db_session, poem):
    from entities import Poem
    poem = Poem(**poem)
    print(f"adding new poem: {poem.id}")
    db_session.add(poem)
    return poem


def add_new_poet_and_poem(db_session, poet_and_poem):
    from entities import PoetAndPoem
    db_session.add(PoetAndPoem(**poet_and_poem))
    print("PoetAndPoem added..")


def poems_handler(poems=None):
    if poems is None:
        return
    try:
        db_session = initialize_session()
        for index, poem in poems.iterrows():

            era = get_existing_era(db_session, poem['poemEra'])
            print(f'era from the database is: {era}')
            if not era:
                add_new_era(db_session, era_name=poem['poemEra'])
                era = get_existing_era(db_session, poem['poemEra'])
            poem['poemEra'] = era.id

            poem_topic = get_existing_poem_topic(db_session, poem['poemTopics'])
            print(f'poem_topic from the database is: {poem_topic}')
            if not poem_topic:
                add_new_poem_topic(db_session, topic_name=poem['poemTopics'])
                poem_topic = get_existing_poem_topic(db_session, poem['poemTopics'])
            poem['poemTopics'] = poem_topic.poemTopicId

            poem_language = get_existing_poem_language(db_session, poem['language'])
            print(f'poem_language from the database is: {poem_language}')
            if not poem_language:
                add_new_poem_language(db_session, language_name=poem['language'])
                poem_language = get_existing_poem_language(db_session, poem['language'])
            poem['language'] = poem_language.languageId

            special_tag = get_existing_special_tag(db_session, poem['poemSpecialTags'])
            print(f'special_tag from the database is: {special_tag}')
            if not special_tag:
                add_new_special_tag(db_session, special_tag_name=poem['poemSpecialTags'])
                special_tag = get_existing_special_tag(db_session, poem['poemSpecialTags'])
            poem['poemSpecialTags'] = special_tag.specialTagId

            poem_types = None
            for poem_type in str(poem['poemTypes']).split(', '):
                db_poem_type = get_existing_poem_type(db_session, poem_type)
                print(f'poem_type from the database is: {db_poem_type}')
                if not db_poem_type:
                    add_new_poem_type(db_session, type_name=poem_type)
                    db_poem_type = get_existing_poem_type(db_session, poem_type)
                if poem_types:
                    poem_types = f"{poem_types}, {db_poem_type.poemTypeId}"
                else:
                    poem_types = db_poem_type.poemTypeId
            poem['poemTypes'] = poem_types

            db_poem = add_new_poem(db_session, poem)
            add_new_poet_and_poem(db_session, {
                "id": str(uuid.uuid4()),
                "poemId": db_poem.id,
                "poetId": poem['poetId'],
            })

        commit_and_destroy_session(db_session)

    except Exception as e:
        print(f"Error: {e}")
        destroy_session()  # Destroy the session in case of an error too


poem_type = "classical, pop"
