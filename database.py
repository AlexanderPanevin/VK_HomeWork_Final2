import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import password,db

DSN = 'postgresql://postgres:'+password+'@localhost:5432/'+db
Base = declarative_base()

engine = sq.create_engine(DSN)
connect = engine.connect()
Session = sessionmaker(bind=engine)

class DB_User(Base):
    __tablename__ = 'DB_user'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(100), unique=True)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)