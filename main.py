from database.db_connection import DBManager
from database.agent_db import AgentDB
from database.mission_db import MissionDB


db = DBManager()

db.create_database()
db.create_tables()




