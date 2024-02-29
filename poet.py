
from sqlalchemy import and_
import pandas as pd
import math

def process_phone_number(phone_number):
    if math.isnan(phone_number):
        return "0"
    else:
        return str(phone_number)

def poets_handler(poets=None):
    if poets is None:
        return 
    try:
        from database import Session
        Session.create_session()
        from entities import Poet

        db_session = Session.session.get_session()

        for index, poet in poets.iterrows():  # Iterate over the rows of the DataFrame
            print('poet', poet)
            check_exists = db_session.query(Poet).filter(
                and_(
                    Poet.firstName == poet['First Name'],
                    Poet.middleName == poet['middleName'],
                    Poet.lastName == poet['lastName']
                )
            ).first()
            if not check_exists:
                print("Create poet ", poet)
                pt = Poet(
                    first_name=poet['firstName'], middle_name=poet['middleName'], last_name=poet['lastName'], 
                    website=poet['website'], address=poet['address'], email=poet['email'], 
                    phone_num=process_phone_number(poet['phoneNumber']),
                    city=poet['city'], status=poet['status'], zip_code=poet['zipCode'], 
                    pic=poet['pic'], is_laureate=poet['isLaureate'] == 'Yes' if True else False, photo_credit=poet['photoCredit'],
                    state=poet['state']
                )
                db_session.add(pt)
            else:
                print("Already Exists data")
        
        db_session.commit()
        Session.session.destroy_session()

    except Exception as e:
        print(f"Error: {e}")
        Session.session.destroy_session()  # Destroy the session in case of error too

