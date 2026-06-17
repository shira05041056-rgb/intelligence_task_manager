from db_connection import DBManager
from utils.utils import chek_rank



class AgentDB:
    def __init__(self, db: DBManager ):
        self.db = db

    def create_agent(self, data):
        if chek_rank(data["agent_rank"]):
            curser = self.db.get_connection().cursor(dictionary=True)
            curser.execute("""INSERT INTO agents (name, specialty, agent_rank)
                        VALUES (%s, %s, %s)""",(data["name"], data["specialty"], data["agent_rank"]))
            curser._connection.commit()
            curser.execute("""SELECT * FROM agents ORDER BY id DESC LIMIT 1""")
            res = curser.fetchone()
            curser.close()
            return res
        return "ERROR: rank must be- Low/Junior/Senior/Commander"
    
    def get_all_agents(self):
        curser = self.db.get_connection().cursor(dictionary=True)
        curser.execute("""SELECT * FROM agents""")
        res = curser.fetchall()
        curser.close()
        return res
    
    def get_agent_by_id(self, id):
        curser = self.db.get_connection().cursor(dictionary=True)
        curser.execute("""SELECT * FROM agents where id = %s""", (id,))
        res = curser.fetchone()
        curser.close()
        return res
    
    def update_agent(self, id, data):
        curser = self.db.get_connection().cursor(dictionary=True)
        curser.execute("""UPDATE agents SET 
                       name=%s, 
                       specialty=%s, 
                       specialty=%s 
                       WHERE id=%s""",(data.name, data.specialty, data.specialty, id))
        curser._connection.commit()
        curser.close()
        return True
    
    def deactivate_agent(self,id):
        curser = self.db.get_connection().cursor(dictionary=True)
        curser.execute("""UPDATE agents SET is_active=False WHERE id=%s""",(id,))
        curser._connection.commit()
        curser.close()
        return True
    
    def increment_completed(self, id):
        curser = self.db.get_connection().cursor(dictionary=True)
        curser.execute("""UPDATE agents SET completed_missions= completed_missions +1 WHERE id=%s""",(id,))
        curser._connection.commit()
        curser.close()
        return True
    
    def increment_failed(self, id):
        curser = self.db.get_connection().cursor(dictionary=True)
        curser.execute("""UPDATE agents SET failed_missions= failed_missions +1 WHERE id=%s""",(id,))
        curser._connection.commit()
        curser.close()
        return True
    
    def get_agent_performance(self, id):
        curser = self.db.get_connection().cursor(dictionary=True)
        curser.execute("""SELECT completed_missions FROM agents WHERE id=%s""",(id,))
        completed = curser.fetchone()
        curser.execute("""SELECT failed_missions FROM agents WHERE id=%s""",(id,))
        failed = curser.fetchone()
        curser.close()
        curser.execute("""SELECT count(*) assigned_agent_id FROM missions WHERE id=%s""",(id,))
        total = curser.fetchone()
        success_rate = completed / total * 100
        return {
            "completed": completed,
            "failed": failed,
            "total": total["count(*)"],
            "success_rate": success_rate
        }

    def count_active_agents(self):
        curser = self.db.get_connection().cursor(dictionary=True)
        curser.execute("""SELECT count(*) as COUNT FROM agents where is_active=True""")
        res = curser.fetchall()
        curser.close()
        return res
