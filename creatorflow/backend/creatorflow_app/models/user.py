from pydantic import BaseModel, Field
from typing import List, Optional


class User(BaseModel):
	id: Optional[str] = None
	email: str
	name: Optional[str] = None
	roles: List[str] = Field(default_factory=lambda: ["editor"])