from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class PlatformVariant(BaseModel):
	platform: str
	caption: str
	hashtags: List[str] = Field(default_factory=list)
	media_urls: List[str] = Field(default_factory=list)
	metadata: Dict[str, str] = Field(default_factory=dict)


class ContentItem(BaseModel):
	id: Optional[str] = None
	brand_id: str
	title: str
	status: str = Field(default="DRAFT")
	brief: Optional[str] = ""
	variants: List[PlatformVariant] = Field(default_factory=list)
	created_at: datetime = Field(default_factory=datetime.utcnow)
	updated_at: datetime = Field(default_factory=datetime.utcnow)
	ab_group: Optional[str] = None
	metrics: Dict[str, float] = Field(default_factory=dict)