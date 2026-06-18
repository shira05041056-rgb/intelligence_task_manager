from fastapi import APIRouter
from database.agent_db import AgentDB
from database.db_connection import DBManager
from utils.service import chek_rank
from pydantic import BaseModel
from typing import Literal

class Agent(BaseModel):
    name: str
    specialty: str
    agent_rank: Literal["Low", "Junior", "Junior", "Commander"]

router = APIRouter(prefix="agents", tags=["agents"])

db = DBManager()


@router.post("/")
def create_agent(data: Agent):
    return AgentDB(db).create_agent(data)

@router.get("/")
def get_all_agents():
    return AgentDB(db).get_all_agents()

@router.get("/{id}")
def get_agent_by_id(id: int):
    return AgentDB(db).get_agent_by_id(id)

@router.put("/{id}")
def update_agent(id: int):
    return AgentDB(db).update_agent()

@router.put("/{id}/deactivate")
def deactivate_agent(id: int):
    return AgentDB(db).deactivate_agent(id)

@router.put("/{id}/performance")
def get_agent_performance(id: int):
    return AgentDB(db).get_agent_performance(id)
