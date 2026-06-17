from db_connection import DBManager
from utils.utils import risk_level_chek



class MissionDB:
    def __init__(self, db: DBManager):
        self.db = db

    def create_mission(self, data):
        risk_level = risk_level_chek(data.difficulty, data.importance)
        curser = self.db.get_connection().cursor(dictionary=True)
        curser.execute("""INSERT INTO missions (title, description, location, difficulty, importance, risk_level)
                    VALUES (%s, %s, %s, %s, %s, %s)""",(data.title, data.description, data.location, data.difficulty, data.importance, risk_level))
        curser._connection.commit()
        curser.execute("""SELECT * FROM missions ORDER BY id DESC LIMIT 1""")
        res = curser.fetchone()
        return res
    
    def get_all_missions(self):
        curser = self.db.get_connection().cursor(dictionary=True)
        curser.execute("""SELECT * FROM missions""")
        res = curser.fetchall()
        curser.close()
        return res
    
    def get_mission_by_id(self, id):
        curser = self.db.get_connection().cursor(dictionary=True)
        curser.execute("""SELECT * FROM missions where id = %s""", (id,))
        res = curser.fetchone()
        curser.close()
        return res
    
    def assign_mission(self, m_id, a_id):
        curser = self.db.get_connection().cursor(dictionary=True)
        curser.execute("""UPDATE mission SET assigned_agent_id =%s WHERE id= %s""",(a_id, m_id))
        curser._connection.commit()
        curser.close()
        return True
    
    def update_mission_status(self, id, status):
        curser = self.db.get_connection().cursor(dictionary=True)
        curser.execute("""UPDATE mission SET status =%s WHERE id= %s""",(status, id))
        curser._connection.commit()
        curser.close()
        return True
    
    def get_open_missions_by_agent(self, id):
        curser = self.db.get_connection().cursor(dictionary=True)
        curser.execute("""SELECT title FROM missions where id = %s""", (id,))
        res = curser.fetchall()
        curser.close()
        return res
    
    def count_all_missions(self):
        curser = self.db.get_connection().cursor(dictionary=True)
        curser.execute("""SELECT count(*) as COUNT FROM missions""")
        res = curser.fetchone()
        curser.close()
        return res
    
    def count_by_status(self, status):
        curser = self.db.get_connection().cursor(dictionary=True)
        curser.execute("""SELECT count(*) as %s FROM missions where status=%s""",(status,))
        res = curser.fetchone()
        curser.close()
        return res
    
    def count_open_missions(self):
        curser = self.db.get_connection().cursor(dictionary=True)
        curser.execute("""SELECT count(*) as open_missions FROM missions where status=New or status=IN_PROGRESS OR status=ASSIGEND""")
        res = curser.fetchone()
        curser.close()
        return res
    
    def count_critical_missions(self):
        curser = self.db.get_connection().cursor(dictionary=True)
        curser.execute("""SELECT count(*) as critical_missions FROM missions where risk_level=CRITICAL""")
        res = curser.fetchone()
        curser.close()
        return res
    
    def get_top_agent(self):
        curser = self.db.get_connection().cursor(dictionary=True)
        curser.execute("""SELECT * FROM missions ORDER BY completed_missions DESC LIMIT 1""")
        res = curser.fetchone()
        curser.close()
        return res

