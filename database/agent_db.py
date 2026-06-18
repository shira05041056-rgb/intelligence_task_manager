from database.db_connection import DBManager
from utils.service import chek_rank



class AgentDB:
    def __init__(self, db: DBManager ):
        self.db = db

    def create_agent(self, data):
        try:
            curser = self.db.get_connection().cursor(dictionary=True)
            curser.execute("""INSERT INTO agents (name, specialty, agent_rank)
            VALUES (%s, %s, %s)""",(data.name, data.specialty, data.agent_rank))
            curser._connection.commit()
            curser.execute("""SELECT * FROM agents ORDER BY id DESC LIMIT 1""")
            res = curser.fetchone()
            return res
        except Exception as e:
            return e
        finally:
            curser.close()
        
    
    def get_all_agents(self):
        try:
            curser = self.db.get_connection().cursor(dictionary=True)
            curser.execute("""SELECT * FROM agents""")
            res = curser.fetchall()
            return res
        except Exception as e:
                return e
        finally:
                curser.close()
    
    def get_agent_by_id(self, id):
        try:
            curser = self.db.get_connection().cursor(dictionary=True)
            curser.execute("""SELECT * FROM agents where id = %s""", (id,))
            res = curser.fetchone()
            return res
        except Exception as e:
            return e
        finally:
            curser.close()

    def update_agent(self, id, data):
        try:
            curser = self.db.get_connection().cursor(dictionary=True)
            curser.execute("""UPDATE agents SET 
                        name=%s, 
                        specialty=%s, 
                        specialty=%s 
                        WHERE id=%s""",(data.name, data.specialty, data.specialty, id))
            curser._connection.commit()
            return True
        except Exception as e:
            return e
        finally:
            curser.close()

    def deactivate_agent(self,id):
        try:
            curser = self.db.get_connection().cursor(dictionary=True)
            curser.execute("""UPDATE agents SET is_active=False WHERE id=%s""",(id,))
            curser._connection.commit()
            return True
        except Exception as e:
            return e
        finally:
            curser.close()
    
    def increment_completed(self, id):
        try:
            curser = self.db.get_connection().cursor(dictionary=True)
            curser.execute("""UPDATE agents SET completed_missions= completed_missions +1 WHERE id=%s""",(id,))
            curser._connection.commit()
            return True
        except Exception as e:
            return e
        finally:
            curser.close()
    
    def increment_failed(self, id):
        try:
            curser = self.db.get_connection().cursor(dictionary=True)
            curser.execute("""UPDATE agents SET failed_missions= failed_missions +1 WHERE id=%s""",(id,))
            curser._connection.commit()
            return True
        except Exception as e:
            return e
        finally:
            curser.close()
    
    def get_agent_performance(self, id):
        try:
            curser = self.db.get_connection().cursor(dictionary=True)
            curser.execute("""SELECT completed_missions FROM agents WHERE id=%s""",(id,))
            completed = curser.fetchone()
            curser.execute("""SELECT failed_missions FROM agents WHERE id=%s""",(id,))
            failed = curser.fetchone()
            curser.execute("""SELECT count(*) assigned_agent_id FROM missions WHERE id=%s""",(id,))
            total = curser.fetchone()
            if total["assigned_agent_id"] > 0:
                success_rate = completed["completed_missions"] / total["assigned_agent_id"] * 100
            else:
                success_rate = 0
            res = {
                "completed": completed["completed_missions"],
                "failed": failed["failed_missions"],
                "total": total["assigned_agent_id"],
                "success_rate": success_rate
            }
            return res
        except Exception as e:
            return e
        finally:
            curser.close()

    def count_active_agents(self):
        try:
            curser = self.db.get_connection().cursor(dictionary=True)
            curser.execute("""SELECT count(*) as COUNT FROM agents where is_active=True""")
            res = curser.fetchone()
            return res["COUNT"]
        except Exception as e:
            return e
        finally:
            curser.close()
