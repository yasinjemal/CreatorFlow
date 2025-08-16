from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class BrandAsset(BaseModel):
	name: str
	url: str
	type: str = Field(description="logo|font|color|template|other")


class BrandProfile(BaseModel):
	id: Optional[str] = None
	owner_user_id: Optional[str] = None
	name: str
	description: Optional[str] = ""
	voice_characteristics: List[str] = Field(default_factory=list)
	tone_guidelines: Dict[str, str] = Field(default_factory=dict)
	style_guide: Dict[str, str] = Field(default_factory=dict)
	primary_colors: List[str] = Field(default_factory=list)
	fonts: List[str] = Field(default_factory=list)
	assets: List[BrandAsset] = Field(default_factory=list)
	blocked_words: List[str] = Field(default_factory=list)
	preferred_hashtags: List[str] = Field(default_factory=list)
	enabled_platforms: List[str] = Field(default_factory=lambda: ["instagram","tiktok","youtube","linkedin","twitter","facebook","pinterest"])