import databases
import sqlalchemy

database = databases.Database("sqlite:///sqlite.db")
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine("sqlite:///sqlite.db")