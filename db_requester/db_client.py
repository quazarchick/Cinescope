from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from resources.db_creds import DatabaseCreds

USERNAME = DatabaseCreds.USER
PASSWORD = DatabaseCreds.PASSWORD
HOST = DatabaseCreds.HOST
PORT = DatabaseCreds.PORT
DATABASE_NAME = DatabaseCreds.NAME

# движок для подключения к базе данных
engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}", echo=False
)

# создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    '''Создаем новую сессию БД'''
    return SessionLocal()

