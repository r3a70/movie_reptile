from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("mysql+mysqldb://root:ram1999@database/movieCrawl", echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()
