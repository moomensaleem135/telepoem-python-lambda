
def poem_collections_handler(poem_collections=None):
    if poem_collections is None:
        return 
    try:
        from database import Session
        Session.create_session()
        from entities import PoemCollection
        Session.create_session()  # Create a database session
        db_session = Session.session.get_session()  # Get the session object

        for index, poem_collection in poem_collections.iterrows():
            print('Poem Collection:', poem_collection)

            check_exists = db_session.query(PoemCollection).filter(
                PoemCollection.name == poem_collection['name']
            ).first()

            if not check_exists:
                print("Creating new PoemCollection:", poem_collection)
                new_poem_collection = PoemCollection(
                    name=poem_collection['name'],
                    description=poem_collection['description'],
                    filterExplicitLanguage=poem_collection['filterExplicitLanguage'],
                    filterAdultContent=poem_collection['filterAdultContent'],
                    dynamicQueryParams=poem_collection['dynamicQueryParams'],
                    dynamicQuery=poem_collection['dynamicQuery'],
                    createdAt=poem_collection['createdAt'],
                    updatedAt=poem_collection['updatedAt'],
                    deletedAt=poem_collection['deletedAt']
                )
                db_session.add(new_poem_collection)
            else:
                print("Updating existing PoemCollection:", poem_collection)
                check_exists.name = poem_collection['name']
                check_exists.description = poem_collection['description']
                check_exists.filterExplicitLanguage = poem_collection['filterExplicitLanguage']
                check_exists.filterAdultContent = poem_collection['filterAdultContent']
                check_exists.dynamicQueryParams = poem_collection['dynamicQueryParams']
                check_exists.dynamicQuery = poem_collection['dynamicQuery']
                check_exists.createdAt = poem_collection['createdAt']
                check_exists.updatedAt = poem_collection['updatedAt']
                check_exists.deletedAt = poem_collection['deletedAt']

        db_session.commit()  # Commit the changes to the database
        Session.session.destroy_session()  # Destroy the session

    except Exception as e:
        print(f"Error: {e}")
        Session.session.destroy_session()  # Destroy the session in case of error too
