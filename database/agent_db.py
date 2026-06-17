from database.db_connection import DBManager



class AgentDB:
    def __init__(self, db: DBManager ):
        self.db = db

    def create_agent(self, data):
        curser = self.db.get_connection().cursor(dictionary=True)
        curser.execute("""INSERT INTO agents (name, specialty, agent_rank)
                    VALUES (%s, %s, %s)""",(data.name, data.specialty, data.agent_rank))
        curser._connection.commit()
        curser.execute("""SELECT LAST ROW id""")
        res = curser.fetchone()

        curser.close()
        return res
    
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
        curser.execute("""SELECT completed_missions FROM agents WHERE id=%s"""(id,))
        completed = curser.fetchone()
        curser.execute("""SELECT failed_missions FROM agents WHERE id=%s"""(id,))
        failed = curser.fetchone()
        curser.close()
        total = completed + failed
        success_rate = completed / total * 100
        return {
            "completed": completed,
            "failed": failed,
            "total": total,
            "success_rate": success_rate
        }

    def count_active_active(self):
        curser = self.db.get_connection().cursor(dictionary=True)
        curser.execute("""SELECT count(*) FROM agents where is_active=True""")
        res = curser.fetchall()
        curser.close()
        return res["COUNT(*)"]

    