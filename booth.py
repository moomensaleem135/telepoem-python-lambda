

def booths_handler(booths=None):
    if booths is None:
        return 
    try:
        from database import Session
        Session.create_session()
        from entities import Booth

        db_session = Session.session.get_session()

        for index, booth_row in booths.iterrows():  # Iterate over the rows of the DataFrame
            print('Booth:', booth_row)
            check_exists = db_session.query(Booth).filter(
                Booth.boothName == booth_row['boothName']
            ).first()
            if not check_exists:
                print("Create booth:", booth_row)
                booth = Booth(
                    boothName=booth_row['boothName'],
                    number=booth_row['number'],
                    phoneTypeId=booth_row['phoneTypeId'],
                    boothTypeId=booth_row['boothTypeId'],
                    directoryTypeId=booth_row['directoryTypeId'],
                    directoryTabletSerialNumber=booth_row['directoryTabletSerialNumber'],
                    physicalAddress=booth_row['physicalAddress'],
                    updateDate=booth_row['updateDate'],
                    city=booth_row['city'],
                    state=booth_row['state'],
                    zip=booth_row['zip'],
                    installationDate=booth_row['installationDate'],
                    installationType=booth_row['installationType'],
                    active=booth_row['active'],
                    isAdaAccessible=booth_row['isAdaAccessible'],
                    phoneSerialNumber=booth_row['phoneSerialNumber'],
                    highlightedCriteria=booth_row['highlightedCriteria'],
                    installationNotes=booth_row['installationNotes'],
                    deviceInfo=booth_row['deviceInfo'],
                    createdAt=booth_row['createdAt'],
                    updatedAt=booth_row['updatedAt'],
                    deletedAt=booth_row['deletedAt'],
                    boothMaintainerId=booth_row['boothMaintainerId']
                )
                db_session.add(booth)
            else:
                print("Booth already exists")

        db_session.commit()
        Session.session.destroy_session()

    except Exception as e:
        print(f"Error: {e}")
        Session.session.destroy_session()  # Destroy the session in case of error too
