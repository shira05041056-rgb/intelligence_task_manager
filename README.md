## System description.

This is a system for managing agents and tasks, using a MySQL data layer and OOP classes that manage the data.\
In the data layer there are two tables:
- agents
- missions

## Folder structure.

intelligence-task-manager/\
├── database\
│ ├── db_connection.py\
│ ├── agent_db.py\
│ └── mission_db.py\
├── README.md\
├── requirements.txt\
└── .gitignore


## The structure of the tables.

### agents:


| field | type |
| ----- | ----: |
| id | INT, AUTO_INCREMENT, PK |
| name | VARCHAR(50) |
| specialty | VARCHAR(50) |
| is_active | BOOLEAN |
| completed_missions | INT |
| failed_missions | INT |
| agent_rank | ENUM |


### missions:

| field | type |
| ----- | ----: |
| id | INT, AUTO_INCREMENT, PK |
| title | VARCHAR(50) |
| description | TEXT |
| location | VARCHAR(50) |
| difficulty | INT |
| importance | INT |
| status | VARCHAR(50) |
| level_risk | VARCHAR(50) |
| assigned_agent_id | INT |

## Explanation of the classes.

### DB_connection:

This is a class whose job is to manage the connection to MySQL, and it has 3 methods.

- get_connection() = Returns an active connection to MySQL.
- create_database() = Creates db_Intelligence if it does not exist.
- create_tables() = Creates both tables if they do not exist.


### AgentDB:

Responsible for all SQL operations against the agents table.

- create_agent(data) = Creates a new agent and returns the agent object.
- get_all_agents() = Returns a list of all agents.
- get_agent_by_id(id) = Returns one agent by ID, or None.
- update_agent(id, data) = UPDATE for the entire row (it is not possible to change the id).
- deactivate_agent(id) = Sets agent status to inactive.
- increment_completed(id) = Updates the number of tasks completed.
- increment_failed(id) = Updates the number of failed tasks.
- get_agent_performance(id) = Returns a dictionary with these keys: completed, failed, total, success_rate.
- count_active_agents() = Returns the number of active agents.

### MissionDB:

Responsible for all SQL operations against the missions table.


- create_mission(data) = Creates a new task and returns the entire object.
- get_all_missions() = Returns all tasks.
- get_mission_by_id(id) = Returns one task by ID, or None.
- assign_mission(m_id, a_id) = Assigning a task to an agent.
- update_mission_status(id, status) = Used for any status change.
- get_open_missions_by_agent(id) = Returns an agent's ASSIGNED/IN PROGRESS tasks.
- count_all_missions() = Total tasks.
- count_by_status(status) = Counting by a certain status.
- count_open_missions() = Open task counter.
- count_critical_missions() = CRITICAL task counter.
- get_top_agent() = The agent with the highest completed_missions.

## System rules.

| Law number | The law |
| ----- | ----: |
| 1 |  Rank must be - Commander / Senior / Junior |
| 2 | Difficulty and importance must be between 1 and 10. |
| 3 | risk_level is automatically calculated when a task is created — the user does not submit it. |
| 4 | An agent with is_active=False cannot accept tasks. |
| 5 | An agent cannot have more than 3 open tasks (PROGRESS_IN / ASSIGNED) at the same time. | 
| 6 | If risk_level=CRITICAL — only an agent with the rank of Commander can accept the mission. |
| 7 | Only a task with a status of NEW can be assigned. After assignment: status=ASSIGNED. |
| 8 | Only a task with the ASSIGNED status can be started. After: status=IN_PROGRESS. |
| 9 | Only a task can be completed - IN_PROGRESS, and changed to completed or failed status. |
| 10 | You can only cancel a task in the NEW or ASSIGNED status. |


## Running instructions:

### Docker:
~~~
docker run --name intelligence-mysql  -e MYSQL_ROOT_PASSWORD=1234  -e MYSQL_DATABASE=Intelligence_db  -p 3306:3306  -v exam_data:/var/lib/mysql  -d mysql:latest
~~~
### project:
~~~
git clone https://github.com/shira05041056-rgb/intelligence_task_manager.git
~~~
### The DB layer:
~~~
python main.py
~~~