from fastapi import APIRouter, HTTPException
from database.mission_db import MissionDB
from database.agent_db import AgentDB
from database.db_connection import DBManager
from utils.service import chek_rank, chek_difficulty_and_importance
from pydantic import BaseModel

class Mission(BaseModel):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    difficulty: int | None = None
    importance: int | None = None

router = APIRouter(prefix="/missions", tags=["missions"])

db = DBManager()


@router.post("/")
def create_mission(data: Mission):
    if chek_difficulty_and_importance(data.difficulty, data.importance):
        raise HTTPException(status_code=400, detail="must be between 1 > 10")
    if not data.title and not data.description and not data.location and not data.difficulty and not data.importance:
            raise HTTPException(status_code=422, detail="cannot be empty!.")
    if not data.title:
            raise HTTPException(status_code=422, detail="Must enter a title!.")
    if not data.description:
            raise HTTPException(status_code=422, detail="Must enter a description!.")
    if not data.location:
            raise HTTPException(status_code=422, detail="Must enter a location!.")
    if not data.difficulty:
            raise HTTPException(status_code=422, detail="Must enter a difficulty!.")
    if not data.importance:
            raise HTTPException(status_code=422, detail="Must enter a importance!.")
    
    return MissionDB(db).create_mission(data)

@router.get("/")
def get_all_missions():
    return MissionDB(db).get_all_missions()

@router.get("/{id}")
def get_mission_by_id(id: int):
    res = MissionDB(db).get_mission_by_id(id)
    if not res:
        raise HTTPException(status_code=404, detail="mission not found.")
    return MissionDB(db).get_mission_by_id(id)

@router.put("/{id}/assign/{agent_id}")
def assign_mission(id: int, agent_id: int):
    m = MissionDB(db).get_mission_by_id(id)
    if not m:
        raise HTTPException(status_code=404, detail="mission not found.")
    a = AgentDB(db).get_agent_by_id(id)
    if not a:
        raise HTTPException(status_code=404, detail="Agent not found.")
    if m["status"] != "NEW":
        raise HTTPException(status_code=400, detail="status not new.")
    if a["is_active"] == 0:
        raise HTTPException(status_code=400, detail="agent not active.")
    res = MissionDB(db).get_open_missions_by_agent(id)
    n = 0
    for d in res:
        n += 1
    if n >= 3:
        raise HTTPException(status_code=400, detail="more from 3 missions for agent.")
    
    
    return MissionDB(db).assign_mission(id, agent_id)

@router.put("/{id}/start")
def starting_mission(id: int):
    return MissionDB(db).update_mission_status(id, "IN_PROGRESS")

@router.put("/{id}/complete")
def conplete_mission(id: int):
    return MissionDB(db).update_mission_status(id, "COMPLETED")

@router.put("/{id}/fail")
def failed_mission(id: int):
    return MissionDB(db).update_mission_status(id, "FAILED")

@router.put("/{id}/cancel")
def cancel_mission(id: int):
    return MissionDB(db).update_mission_status(id, "CANCELLED")