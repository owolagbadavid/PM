from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, subqueryload

engine = create_engine('postgresql://db:5432/pm?user=postgres')
Session = sessionmaker(bind=engine)
session = Session()
