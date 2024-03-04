from sqlalchemy import and_
import math
from database import destroy_session, commit_and_destroy_session, initialize_session


def process_phone_number(phone_number):
    return "0" if math.isnan(phone_number) else str(phone_number)


def get_existing_poet(db_session, poet):
    from entities import Poet

    return (
        db_session.query(Poet)
        .filter(
            and_(
                Poet.legalLastName == poet["legalLastName"],
                Poet.legalFirstName == poet["legalFirstName"],
            )
        )
        .first()
    )


def update_poet(existing_poet, new_poet):
    from entities import Poet

    new_poet = Poet(**new_poet)
    print("Updating the poet.......")
    if new_poet.poetImage:
        existing_poet.poetImage = new_poet.poetImage
    if new_poet.address:
        existing_poet.address = new_poet.address
    if new_poet.poetBiography:
        existing_poet.poetBiography = new_poet.poetBiography
    if new_poet.creditedFirstName:
        existing_poet.creditedFirstName = new_poet.creditedFirstName
    if new_poet.creditedLastName:
        existing_poet.creditedLastName = new_poet.creditedLastName
    if new_poet.email:
        existing_poet.email = new_poet.email
    if new_poet.state:
        existing_poet.state = new_poet.state
    if new_poet.status:
        existing_poet.status = new_poet.status
    if new_poet.city:
        existing_poet.city = new_poet.city
    if new_poet.isLaureate:
        existing_poet.isLaureate = new_poet.isLaureate
    if new_poet.phoneNumber:
        existing_poet.phoneNumber = new_poet.phoneNumber
    if new_poet.picCredits:
        existing_poet.picCredits = new_poet.picCredits
    if new_poet.website:
        existing_poet.website = new_poet.website
    if new_poet.zip:
        existing_poet.zip = new_poet.zip


def add_new_poet(db_session, poet):
    from entities import Poet

    print("adding new poet......")
    # db_session.add(Poet(**poet))
    new_poet = Poet(**poet)
    db_session.add(new_poet)
    return new_poet


def poets_handler(poets=None):
    if poets is None:
        return []
    try:
        db_session = initialize_session()

        poet_ids = []
        for index, poet in poets.iterrows():
            existing_poet = get_existing_poet(db_session, poet)
            if existing_poet:
                update_poet(existing_poet, poet)
            else:
                existing_poet = add_new_poet(db_session, poet)
                # existing_poet = get_existing_poet(db_session, poet)
            poet_ids.append(existing_poet.id)

        commit_and_destroy_session(db_session)
        return poet_ids

    except Exception as e:
        print(f"Error: {e}")
        destroy_session()  # Destroy the session in case of an error too
