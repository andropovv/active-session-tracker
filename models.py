from pydantic import BaseModel
from datetime import datetime

class Session(BaseModel):
    session_id: str
    start_time: datetime
    user_agent: str
    ip: str
