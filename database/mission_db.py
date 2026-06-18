from database.db_connection import DBManager
from utils.service import risk_level_chek, chek_difficulty_and_importance



class MissionDB:
    def __init__(self, db: DBManager):
        self.db = db

    def create_mission(self, data):
        try:
            risk_level = risk_level_chek(data.difficulty, data.importance)
            curser = self.db.get_connection().cursor(dictionary=True)
            curser.execute("""INSERT INTO missions (title, description, location, difficulty, importance, risk_level)
                        VALUES (%s, %s, %s, %s, %s, %s)""",(data.title, data.description, data.location, data.difficulty, data.importance, risk_level))
            curser._connection.commit()
            curser.execute("""SELECT * FROM missions ORDER BY id DESC LIMIT 1""")
            res = curser.fetchone()
            return res
        except Exception as e:
            return e
        finally:
            curser.close()
    
    def get_all_missions(self):
        try:
            curser = self.db.get_connection().cursor(dictionary=True)
            curser.execute("""SELECT * FROM missions""")
            res = curser.fetchall()
            return res
        except Exception as e:
            return e
        finally:
            curser.close()
    
    def get_mission_by_id(self, id):
        try:
            curser = self.db.get_connection().cursor(dictionary=True)
            curser.execute("""SELECT * FROM missions where id = %s""", (id,))
            res = curser.fetchone()
            return res
        except Exception as e:
            return e
        finally:
            curser.close()
    
    def assign_mission(self, m_id, a_id):
        try:
            curser = self.db.get_connection().cursor(dictionary=True)
            curser.execute("""UPDATE missions SET assigned_agent_id =%s WHERE id= %s""",(a_id, m_id))
            curser._connection.commit()
            return True
        except Exception as e:
            return e
        finally:
            curser.close()
    
    def update_mission_status(self, id, status):
        try:
            curser = self.db.get_connection().cursor(dictionary=True)
            curser.execute("""UPDATE missions SET status =%s WHERE id= %s""",(status, id))
            curser._connection.commit()
            return True
        except Exception as e:
            return e
        finally:
            curser.close()

    def get_open_missions_by_agent(self, id):
        try:
            curser = self.db.get_connection().cursor(dictionary=True)
            curser.execute("""SELECT title FROM missions where id = %s""", (id,))
            res = curser.fetchall()
            return res
        except Exception as e:
            return e
        finally:
            curser.close()
    
    def count_all_missions(self):
        try:
            curser = self.db.get_connection().cursor(dictionary=True)
            curser.execute("""SELECT count(*) FROM missions""")
            res = curser.fetchone()
            return res["count(*)"]
        except Exception as e:
            return e
        finally:
            curser.close()
    
    def count_by_status(self, status):
        try:
            curser = self.db.get_connection().cursor(dictionary=True)
            curser.execute("""SELECT count(*) FROM missions where status=%s""",(status,))
            res = curser.fetchone()
            return res["count(*)"]
        except Exception as e:
            return e
        finally:
            curser.close()
    
    def count_open_missions(self):
        try:
            curser = self.db.get_connection().cursor(dictionary=True)
            curser.execute("""SELECT count(*) FROM missions where status='IN_PROGRESS' or status= 'ASSIGEND'""")
            res = curser.fetchone()
            return res["count(*)"]
        except Exception as e:
            return e
        finally:
            curser.close()
    
    def count_critical_missions(self):
        try:
            curser = self.db.get_connection().cursor(dictionary=True)
            curser.execute("""SELECT count(*) FROM missions where risk_level='CRITICAL'""")
            res = curser.fetchone()
            return res["count(*)"]
        except Exception as e:
            return e
        finally:
            curser.close()
    
    def get_top_agent(self):
        try:
            curser = self.db.get_connection().cursor(dictionary=True)
            curser.execute("""SELECT * FROM agents ORDER BY completed_missions DESC LIMIT 1""")
            res = curser.fetchone()
            return res
        except Exception as e:
            return e
        finally:
            curser.close()

