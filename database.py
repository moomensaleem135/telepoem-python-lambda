        
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# DATABASE_URI = 'postgresql://postgres:postgres@telepoem-database.c5yke2c0u4zj.us-east-1.rds.amazonaws.com:5432/postgres'
DATABASE_URI = os.getenv("DATABASE_URI")
if not all([DATABASE_URI]):
            raise ValueError("DATABASE_URI not providedin .env")

class Session:
    session = None

    @staticmethod
    def create_session():
        Session.session = Session()
        Session.session.init_db()

    def destroy_session(self):
        self.db_session.close()
        self.engine.dispose()

    def get_engine(self):
        return self.engine

    def get_session(self):
        return self.db_session

    def get_base(self):
        return self.Base

    def init_db(self):
        self.engine = create_engine(DATABASE_URI)
        self.db_session = scoped_session(sessionmaker(autocommit=False,
                                                      autoflush=True,
                                                      bind=self.engine))
        self.Base = declarative_base()
        self.Base.query = self.db_session.query_property()
        from entities import Poet, PoetAndPoem, Booth, BoothAndPoemCollection, BoothLoggingHistory, BoothMaintainer, ParticipantSession, Poem, PoemCollection, PoemCollectionAndPoem
        self.Base.metadata.create_all(bind=self.engine)
