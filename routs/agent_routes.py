from fastapi import APIRouter, HTTPException
from database.agent_db import AgentDB
from database.db_connection import DBManager
from utils.service import chek_rank
from pydantic import BaseModel, PydanticUserError
from typing import Literal
from logs.looger import logger

class Agent(BaseModel):
    name: str | None = None
    specialty: str | None = None
    agent_rank: str | None = None

router = APIRouter(prefix="/agents", tags=["agents"])

db = DBManager()


@router.post("/", status_code=201)
def create_agent(data: Agent):
        logger.info("POST create_agent")
        if not data.name and not data.agent_rank and not data.specialty:
            raise HTTPException(status_code=422, detail="Cannot be empty.")
        if not data.name:
            raise HTTPException(status_code=422, detail="Must enter a name!.")
        if not data.agent_rank:
            raise HTTPException(status_code=422, detail="Must enter an agent_rank!.")
        if not data.specialty:
            raise HTTPException(status_code=422, detail="Must enter a specialty!.")
        if not chek_rank(data.agent_rank):
            raise HTTPException(status_code=400, detail="Invalid rank.")
        
        logger.info("agent Created successfully")
        return AgentDB(db).create_agent(data)

        
@router.get("/")
def get_all_agents():
    logger.info("get all agents")
    return AgentDB(db).get_all_agents()

@router.get("/{id}")
def get_agent_by_id(id: int):
    logger.info("get_agent_by_id")
    res = AgentDB(db).get_agent_by_id(id)
    if not res:
        logger.error("Agent not found.")
        raise HTTPException(status_code=404, detail="Agent not found.")
    return AgentDB(db).get_agent_by_id(id)

@router.put("/{id}")
def update_agent(id: int, data: Agent):
    logger.info("update-agent")
    res = AgentDB(db).get_agent_by_id(id)
    if not res:
        logger.error("agent not found")
        raise HTTPException(status_code=404, detail="Agent not found.")
    if not data.name and not data.agent_rank and not data.specialty:
            raise HTTPException(status_code=422, detail="Cannot be empty.")
    
    return AgentDB(db).update_agent(id, data)

@router.put("/{id}/deactivate")
def deactivate_agent(id: int):
    res = AgentDB(db).get_agent_by_id(id)
    if not res:
        raise HTTPException(status_code=404, detail="Agent not found.")
    return AgentDB(db).deactivate_agent(id)

@router.put("/{id}/performance")
def get_agent_performance(id: int):
    res = AgentDB(db).get_agent_by_id(id)
    if not res:
        raise HTTPException(status_code=404, detail="Agent not found.")
    return AgentDB(db).get_agent_performance(id)
