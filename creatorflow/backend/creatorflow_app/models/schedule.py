from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class ScheduleItem(BaseModel):
	id: Optional[str] = None
	content_id: str
	brand_id: str
	platforms: List[str]
	post_at: datetime
	status: str = Field(default="SCHEDULED")
	last_error: Optional[str] = None