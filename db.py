from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text

# engine = create_engine('postgresql://postgres:admin@localhost:5433/postgres')
internal_engine = create_engine('postgresql://database_artesian_ai_monitor_user:nWiyie5KaFy5ZO5pYvaR8hNJVdR0FHHx@dpg-cps1d056l47c73du3610-a/database_artesian_ai_monitor')
external_engine = create_engine('postgresql://database_artesian_ai_monitor_user:nWiyie5KaFy5ZO5pYvaR8hNJVdR0FHHx@dpg-cps1d056l47c73du3610-a.oregon-postgres.render.com/database_artesian_ai_monitor')

Session = sessionmaker(bind=internal_engine)
Base = declarative_base()

def init():
    with open('db_init.txt', 'r') as file:
        db_init = file.read()

    with internal_engine.begin() as connection:
        connection.execute(text(db_init))