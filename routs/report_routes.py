from fastapi import APIRouter
from database.mission_db import MissionDB
from database.db_connection import DBManager
from utils.service import chek_rank
from database.agent_db import AgentDB

router = APIRouter(prefix="/reports", tags=["reports"])

db = DBManager()

@router.get("/summary")
def get_report():
    return {
        "active_agents_count": AgentDB(db).count_active_agents(),
        "total_missions": MissionDB(db).count_all_missions(),
        "open_missions": MissionDB(db).count_open_missions(),
        "completed_missions": MissionDB(db).count_by_status("COMPLETED"),
        "failed_missions": MissionDB(db).count_by_status("FAILED"),
        "critical_missions": MissionDB(db).count_critical_missions()
    }

@router.get("/missions-by-status")
def get_missions_by_status():
    return {
        "open": MissionDB(db).count_open_missions(),
        "in_progress": MissionDB(db).count_by_status("IN_PROGRESS"),
        "completed": MissionDB(db).count_by_status("COMPLETED"),
        "failed": MissionDB(db).count_by_status("FAILED"),
        "canceled": MissionDB(db).count_by_status("CANCELLED")
    }

@router.get("/top-agent")
def get_top_agent():
    return MissionDB(db).get_top_agent()
