from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text

# engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/DW_Server')
engine = create_engine('postgresql://database_artesian_ai_monitor_user:nWiyie5KaFy5ZO5pYvaR8hNJVdR0FHHx@dpg-cps1d056l47c73du3610-a/database_artesian_ai_monitor')
# engine = create_engine('postgresql://postgres:admin@localhost:5433/postgres')
Session = sessionmaker(bind=engine)
Base = declarative_base()

def init():
    with open('db_init.txt', 'r') as file:
        db_init = file.read()

    with engine.begin() as connection:
        connection.execute(text(db_init))