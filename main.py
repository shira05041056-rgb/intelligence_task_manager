import uvicorn
from fastapi import FastAPI
from database.db_connection import DBManager
from database.agent_db import AgentDB
from database.mission_db import MissionDB
from routs import agent_routes, mission_routes, report_routes


app = FastAPI()


DBManager().create_database()
DBManager().create_tables()

app.include_router(agent_routes.router)
app.include_router(mission_routes.router)
app.include_router(report_routes.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)




