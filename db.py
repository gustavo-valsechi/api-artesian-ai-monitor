from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/DW_Server')
engine = create_engine('postgres://artesian_ai_monitor_user:gDL8J60ABfwk4lgHN8NyWSlPSpXtMKf2@dpg-cp6k91mv3ddc73fltqfg-a/artesian_ai_monitor')
Session = sessionmaker(bind=engine)
Base = declarative_base()