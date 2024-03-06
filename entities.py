import uuid
from sqlalchemy import (
    Column,
    String,
    Boolean,
    TIMESTAMP,
    ForeignKey,
    func,
    DateTime,
    Integer,
    Text,
    JSON,
    Date,
)
from sqlalchemy.orm import relationship
from database import Session
from datetime import datetime


#
# class BoothMaintainer(Session.session.get_base()):
#     __tablename__ = 'booth_maintainer'
#
#     id = Column(String, primary_key=True)
#     name = Column(String)
#     phoneNumber = Column(String)
#     email = Column(String)
#     createdAt = Column(DateTime, default=func.now())
#     deletedAt = Column(DateTime, nullable=True)
#     city = Column(String)
#     state = Column(String)
#     zip = Column(String)
#
#     # # Use the foreign key relationship
#     # booth_id = Column(String, ForeignKey('booth.booth_maintainer_id'))
#
#     # booth = relationship("Booth", foreign_keys=[booth_id])
#
#
# class Booth(Session.session.get_base()):
#     __tablename__ = 'booth'
#
#     id = Column(String, primary_key=True, default=str(uuid.uuid4()))
#     boothName = Column(String, nullable=False)
#     number = Column(String, nullable=True)
#     phoneTypeId = Column(String, nullable=True)
#     boothTypeId = Column(String, nullable=True)
#     directoryTypeId = Column(String, nullable=True)
#     directoryTabletSerialNumber = Column(String, nullable=True)
#     physicalAddress = Column(String, nullable=True)
#     updateDate = Column(DateTime, nullable=True)
#     city = Column(String, nullable=True)
#     state = Column(String, nullable=True)
#     zipCode = Column(Integer, nullable=True)
#     installationDate = Column(DateTime, nullable=True)
#     installationType = Column(String, nullable=True)
#     active = Column(Boolean, default=True, nullable=False)
#     isAdaAccessible = Column(Boolean, default=False, nullable=False)
#     phoneSerialNumber = Column(String, nullable=True)
#     highlightedCriteria = Column(String, nullable=True)
#     installationNotes = Column(Text, nullable=True)
#     deviceInfo = Column(Text, nullable=True)
#     createdAt = Column(DateTime, nullable=True, default=datetime.now)
#     updatedAt = Column(DateTime, nullable=True, default=datetime.now, onupdate=datetime.now)
#     deletedAt = Column(DateTime, nullable=True)
#
#     boothMaintainerId = Column(String, ForeignKey('booth_maintainer.id'), unique=True)
#     boothAndPoemCollections = relationship("BoothAndPoemCollection")
#     loggingHistories = relationship("BoothLoggingHistory")
#     sessions = relationship("ParticipantSession")
#     boothMaintainer = relationship("BoothMaintainer")
#
#     def __init__(self, boothName=None, number=None, phoneTypeId=None, boothTypeId=None,
#                  directoryTypeId=None, directoryTabletSerialNumber=None, physicalAddress=None,
#                  updateDate=None, city=None, state=None, zipCode=None, installationDate=None,
#                  installationType=None, active=True, isAdaAccessible=False, phoneSerialNumber=None,
#                  highlightedCriteria=None, installationNotes=None, deviceInfo=None,
#                  createdAt=datetime.now, updatedAt=None, deletedAt=None):
#         self.id = str(uuid.uuid4())
#         self.boothName = boothName
#         self.number = number
#         self.phoneTypeId = phoneTypeId
#         self.boothTypeId = boothTypeId
#         self.directoryTypeId = directoryTypeId
#         self.directoryTabletSerialNumber = directoryTabletSerialNumber
#         self.physicalAddress = physicalAddress
#         self.updateDate = updateDate
#         self.city = city
#         self.state = state
#         self.zipCode = zipCode
#         self.installationDate = installationDate
#         self.installationType = installationType
#         self.active = active
#         self.isAdaAccessible = isAdaAccessible
#         self.phoneSerialNumber = phoneSerialNumber
#         self.highlightedCriteria = highlightedCriteria
#         self.installationNotes = installationNotes
#         self.deviceInfo = deviceInfo
#         self.createdAt = createdAt
#         self.updatedAt = updatedAt
#         self.deletedAt = deletedAt
#
#     def __repr__(self):
#         return f"<Booth(boothName='{self.boothName}', number='{self.number}', city='{self.city}')>"
#
#     def to_json(self):
#         return {
#             "boothName": self.boothName,
#             "number": self.number,
#             "phoneTypeId": self.phoneTypeId,
#             "boothTypeId": self.boothTypeId,
#             "directoryTypeId": self.directoryTypeId,
#             "directoryTabletSerialNumber": self.directoryTabletSerialNumber,
#             "physicalAddress": self.physicalAddress,
#             "updateDate": self.updateDate,
#             "city": self.city,
#             "state": self.state,
#             "zipCode": self.zipCode,
#             "installationDate": self.installationDate,
#             "installationType": self.installationType,
#             "active": self.active,
#             "isAdaAccessible": self.isAdaAccessible,
#             "phoneSerialNumber": self.phoneSerialNumber,
#             "highlightedCriteria": self.highlightedCriteria,
#             "installationNotes": self.installationNotes,
#             "deviceInfo": self.deviceInfo,
#             "createdAt": self.createdAt,
#             "updatedAt": self.updatedAt,
#             "deletedAt": self.deletedAt
#         }
#
#
# class BoothLoggingHistory(Session.session.get_base()):
#     __tablename__ = 'booth_logging_history'
#
#     id = Column(String, primary_key=True)
#     boothId = Column(String, ForeignKey('booth.id'))
#     boothState = Column(String)
#     loggingDateTime = Column(DateTime)
#     active = Column(Boolean)
#
#     booth = relationship("Booth")
#
#
# class PoemCollection(Session.session.get_base()):
#     __tablename__ = 'poem_collection'
#
#     id = Column(String, primary_key=True, default=str(uuid.uuid4()))
#     name = Column(String(255))
#     description = Column(Text)
#     filterExplicitLanguage = Column(Boolean, default=False)
#     filterAdultContent = Column(Boolean, default=False)
#     dynamicQueryParams = Column(JSON, default={})
#     dynamicQuery = Column(Text, default='')
#     createdAt = Column(DateTime, default=datetime.utcnow)
#     updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     deletedAt = Column(DateTime)
#
#     boothAndPoemCollections = relationship("BoothAndPoemCollection", back_populates="poem_collection")
#     poems = relationship("PoemCollectionAndPoem", back_populates="poem_collection")
#
#     def __init__(self, name=None, description=None, filterExplicitLanguage=False, filterAdultContent=False,
#                  dynamicQueryParams=None, dynamicQuery='', createdAt=None, updatedAt=None, deletedAt=None):
#         self.id = str(uuid.uuid4())
#         self.name = name
#         self.description = description
#         self.filterExplicitLanguage = filterExplicitLanguage
#         self.filterAdultContent = filterAdultContent
#         self.dynamicQueryParams = dynamicQueryParams if dynamicQueryParams else {}
#         self.dynamicQuery = dynamicQuery
#         self.createdAt = createdAt if createdAt else datetime.utcnow()
#         self.updatedAt = updatedAt
#         self.deletedAt = deletedAt
#
#     def __repr__(self):
#         return f"<PoemCollection(name='{self.name}', description='{self.description}')>"
#
#     def to_json(self):
#         return {
#             "name": self.name,
#             "description": self.description,
#             "filterExplicitLanguage": self.filterExplicitLanguage,
#             "filterAdultContent": self.filterAdultContent,
#             "dynamicQueryParams": self.dynamicQueryParams,
#             "dynamicQuery": self.dynamicQuery,
#             "createdAt": self.createdAt,
#             "updatedAt": self.updatedAt,
#             "deletedAt": self.deletedAt
#         }
#
#
# class BoothAndPoemCollection(Session.session.get_base()):
#     __tablename__ = 'booth_and_poem_collection'
#
#     id = Column(String, primary_key=True)
#     boothId = Column(String, ForeignKey('booth.id'))
#     poemCollectionId = Column(String, ForeignKey('poem_collection.id'))
#     deletedAt = Column(DateTime, nullable=True)
#
#     booth = relationship("Booth")
#     poemCollection = relationship("PoemCollection")
#
#
# class ParticipantSession(Session.session.get_base()):
#     __tablename__ = 'participant_session'
#
#     id = Column(String, primary_key=True)
#     boothId = Column(String, ForeignKey('booth.id'))
#     dialledPoemNumber = Column(String)
#     durationOfSession = Column(Integer)  # Assuming it's in seconds
#     fullyListened = Column(Boolean)
#     createdAt = Column(DateTime)
#     startedAt = Column(DateTime)
#     endedAt = Column(DateTime)
#     poemId = Column(String, ForeignKey('poem.id'))
#
#     booth = relationship("Booth")
#     poem = relationship("Poem")
#
#
# class PoemCollectionAndPoem(Session.session.get_base()):
#     __tablename__ = 'poem_collection_and_poem'
#
#     id = Column(String, primary_key=True)
#     poemCollectionId = Column(String, ForeignKey('poem_collection.id'))
#     poemId = Column(String, ForeignKey('poem.id'))
#
#     poemCollection = relationship("PoemCollection")
#     poem = relationship("Poem")
#
#
# class CopyRight(Session.session.get_base()):
#     __tablename__ = 'copy_right'
#
#     copyRightId = Column(String, primary_key=True)
#     publicationTitle = Column(String)
#     publisherName = Column(String, nullable=True)
#     publishingDate = Column(String, nullable=True)
#     deletedAt = Column(Date, nullable=True)
#
#     poems = relationship("Poem", back_populates="copy_right")


class Poem(Session.session.get_base()):
    __tablename__ = "poem"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    title = Column(String)
    poetId = Column(String, ForeignKey("poet.id"), nullable=True)
    telepoemNumber = Column(String)
    image = Column(String, nullable=True)
    audioLink = Column(String, nullable=True)
    producerName = Column(String, nullable=True)
    narratorName = Column(String, nullable=True)
    recordingDate = Column(TIMESTAMP(timezone=True), nullable=True)
    recordingSource = Column(String, nullable=True)
    recordingDuration = Column(String, nullable=True)
    era = Column(String, nullable=True)
    type = Column(String, nullable=True)
    topics = Column(String, nullable=True)
    specialTags = Column(String, nullable=True)
    poemText = Column(String)
    language = Column(String)
    copyRights = Column(String)
    active = Column(Boolean, nullable=True)
    optionalLegal = Column(String, nullable=True)
    isChildrenPoem = Column(Boolean, nullable=True)
    isAdultPoem = Column(Boolean, nullable=True)
    # createdAt = Column(TIMESTAMP(timezone=True), default=func.now())
    # updatedAt = Column(TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now())
    deletedAt = Column(TIMESTAMP(timezone=True), nullable=True)

    # poemCollections = relationship("PoemCollectionAndPoem")
    poets = relationship("PoetAndPoem")

    # participantSessions = relationship("ParticipantSession")
    # copyRightId = Column(String, ForeignKey('copy_right.copy_right_id'))
    # copyRight = relationship("CopyRight", back_populates="poems")
    def __init__(
        self,
        title=None,
        poetId=None,
        telepoemNumber=None,
        image=None,
        audioLink=None,
        producerName=None,
        narratorName=None,
        recordingDate=None,
        recordingSource=None,
        recordingDuration=None,
        era=None,
        types=None,
        topics=None,
        specialTags=None,
        poemText=None,
        language=None,
        copyRights=None,
        active=None,
        optionalLegal=None,
        isChildrenPoem=None,
        isAdultPoem=None,
    ):
        self.id = str(uuid.uuid4())
        self.title = title
        self.poetId = poetId
        self.telepoemNumber = telepoemNumber
        self.image = image
        self.audioLink = audioLink
        self.producerName = producerName
        self.narratorName = narratorName
        self.recordingDate = recordingDate
        self.recordingSource = recordingSource
        self.recordingDuration = recordingDuration
        self.poemEra = era
        self.poemTypes = types
        self.poemTopics = topics
        self.poemSpecialTags = specialTags
        self.poemText = poemText
        self.language = language
        self.copyRight = copyRights
        self.active = active
        self.optionalLegal = optionalLegal
        self.isChildrenPoem = isChildrenPoem
        self.isAdultPoem = isAdultPoem


class PoetAndPoem(Session.session.get_base()):
    __tablename__ = "poet_and_poem"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    poemId = Column(String, ForeignKey("poem.id"))
    poetId = Column(String, ForeignKey("poet.id"))

    poem = relationship("Poem")
    poet = relationship("Poet")

    def __init__(self, poemId=None, poetId=None):
        self.id = str(uuid.uuid4())
        self.poemId = poemId
        self.poetId = poetId


class Era(Session.session.get_base()):
    __tablename__ = "era"
    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    name = Column(String)
    deletedAt = Column(Date)

    def __init__(self, name=None, deletedAt=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.deletedAt = deletedAt

    def __repr__(self):
        return f"<Era(id='{self.id}', name='{self.name}')>"


class PoemType(Session.session.get_base()):
    __tablename__ = "poem_type"
    poemTypeId = Column(String, primary_key=True, default=str(uuid.uuid4()))
    name = Column(String)
    deletedAt = Column(Date)

    def __init__(self, name=None, deletedAt=None):
        self.poemTypeId = str(uuid.uuid4())
        self.name = name
        self.deletedAt = deletedAt

    def __repr__(self):
        return f"<PoemType(poemTypeId='{self.poemTypeId}', name='{self.name}')>"


class PoemTopic(Session.session.get_base()):
    __tablename__ = "poem_topic"
    poemTopicId = Column(String, primary_key=True, default=str(uuid.uuid4()))
    name = Column(String)
    deletedAt = Column(Date)

    def __init__(self, name=None, deletedAt=None):
        self.poemTopicId = str(uuid.uuid4())
        self.name = name
        self.deletedAt = deletedAt

    def __repr__(self):
        return f"<PoemTopic(id='{self.poemTopicId}', name='{self.name}')>"


class Language(Session.session.get_base()):
    __tablename__ = "language"
    languageId = Column(String, primary_key=True, default=str(uuid.uuid4()))
    name = Column(String)
    country = Column(String)
    deletedAt = Column(Date)

    def __init__(self, name=None, country=None, deletedAt=None):
        self.languageId = str(uuid.uuid4())
        self.name = name
        self.country = country
        self.deletedAt = deletedAt

    def __repr__(self):
        return f"<Language(languageId='{self.languageId}', name='{self.name}')>"


class SpecialTag(Session.session.get_base()):
    __tablename__ = "special_tag"
    specialTagId = Column(String, primary_key=True, default=str(uuid.uuid4()))
    name = Column(String)
    deletedAt = Column(Date)

    def __init__(self, name=None, deletedAt=None):
        self.specialTagId = str(uuid.uuid4())
        self.name = name
        self.deletedAt = deletedAt

    def __repr__(self):
        return f"<SpecialTag(specialTagId='{self.specialTagId}', name='{self.name}')>"


# class CopyRight(Session.session.get_base()):
#     __tablename__ = 'copy_right'
#     copyRightId = Column(String, primary_key=True, default=str(uuid.uuid4()))
#     publicationTitle = Column(String)
#     publisherName = Column(String)
#     publishingDate = Column(String)
#     deletedAt = Column(Date)
#
#     def __init__(self, publicationTitle=None, publisherName=None, publishingDate=None, deletedAt=None):
#         self.copyRightId = str(uuid.uuid4())
#         self.publicationTitle = publicationTitle
#         self.publisherName = publisherName
#         self.publishingDate = publishingDate
#         self.deletedAt = deletedAt
#
#     def __repr__(self):
#         return f"<CopyRight(id='{self.copyRightId}', publicationTitle='{self.publicationTitle}')>"
#
#
# class PhoneType(Session.session.get_base()):
#     __tablename__ = 'phone_type'
#     id = Column(String, primary_key=True, default=str(uuid.uuid4()))
#     name = Column(String)
#     deletedAt = Column(Date)
#
#     def __init__(self, name=None, deletedAt=None):
#         self.id = str(uuid.uuid4())
#         self.name = name
#         self.deletedAt = deletedAt
#
#     def __repr__(self):
#         return f"<PhoneType(id='{self.id}', name='{self.name}')>"
#
#
# class DirectoryType(Session.session.get_base()):
#     __tablename__ = 'directory_type'
#     id = Column(String, primary_key=True, default=str(uuid.uuid4()))
#     name = Column(String)
#     deletedAt = Column(Date)
#
#     def __init__(self, name=None, deletedAt=None):
#         self.id = str(uuid.uuid4())
#         self.name = name
#         self.deletedAt = deletedAt
#
#     def __repr__(self):
#         return f"<DirectoryType(id='{self.id}', name='{self.name}')>"
#
#
# class TelepoemBoothType(Session.session.get_base()):
#     __tablename__ = 'telepoem_booth_type'
#     id = Column(String, primary_key=True, default=str(uuid.uuid4()))
#     name = Column(String)
#     deletedAt = Column(Date)
#
#     def __init__(self, name=None, deletedAt=None):
#         self.id = str(uuid.uuid4())
#         self.name = name
#         self.deletedAt = deletedAt
#
#     def __repr__(self):
#         return f"<TelepoemBoothType(id='{self.id}', name='{self.name}')>"


class Poet(Session.session.get_base()):
    __tablename__ = "poet"
    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    website = Column(String, nullable=True)
    address = Column(String, nullable=True)
    email = Column(String)
    phoneNum = Column(String)
    city = Column(String)
    status = Column(Boolean)
    zipCode = Column(String)
    isLaureate = Column(Boolean)
    photoCredit = Column(String, nullable=True)
    state = Column(String)
    deletedAt = Column(TIMESTAMP, nullable=True)
    legalFirstName = Column(String)
    legalLastName = Column(String)
    creditedFirstName = Column(String)
    creditedLastName = Column(String)
    poetImage = Column(String, nullable=True)
    poetBiography = Column(String)

    # createdAt = Column(TIMESTAMP, default=datetime.utcnow)
    # updatedAt = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define One-to-Many relationship with PoetAndPoem entity
    poets = relationship("PoetAndPoem", back_populates="poet")

    def __init__(
        self,
        website=None,
        address=None,
        email=None,
        phoneNum=None,
        city=None,
        status=None,
        zipCode=None,
        isLaureate=None,
        photoCredit=None,
        state=None,
        deletedAt=None,
        legalFirstName=None,
        legalLastName=None,
        creditedFirstName=None,
        creditedLastName=None,
        poetImage=None,
        poetBiography=None,
        createdAt=datetime.utcnow,
        updatedAt=None,
    ):
        self.id = str(uuid.uuid4())
        self.website = website
        self.address = address
        self.email = email
        self.phoneNum = phoneNum
        self.city = city
        self.status = status
        self.zipCode = zipCode
        self.isLaureate = isLaureate
        self.photoCredit = photoCredit
        self.state = state
        self.legalFirstName = legalFirstName
        self.legalLastName = legalLastName
        self.creditedFirstName = creditedFirstName
        self.creditedLastName = creditedLastName
        self.poetImage = poetImage
        self.poetBiography = poetBiography
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.deletedAt = deletedAt

    # def __repr__(self):
    #     return f"<Poet(first_name='{self.firstName}', middle_name='{self.middleName}' lastName='{self.last_name}', email='{self.email}')>"

    # def to_json(self):
    #     return {
    #         "firstName": self.firstName,
    #         "middleName": self.middleName,
    #         "lastName": self.lastName,
    #         "website": self.website,
    #         "address": self.address,
    #         "email": self.email,
    #         "phone_num": self.phoneNumber,
    #         "city": self.city,
    #         "status": self.status,
    #         "zipCode": self.zipCode,
    #         "pic": self.pic,
    #         "isLaureate": self.isLaureate,
    #         "picCredits": self.picCredits,
    #         "state": self.state,
    #         "createdAt": self.createdAt,
    #         "updatedAt": self.updatedAt,
    #         "deletedAt": self.deletedAt
    #     }
