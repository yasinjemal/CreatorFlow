from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


class AppSettings(BaseSettings):
	secret_key: str = Field(default="change-me")
	jwt_secret: str = Field(default="change-me-jwt")
	mongo_uri: str = Field(default="mongodb://root:example@mongo:27017/creatorflow?authSource=admin")
	redis_url: str = Field(default="redis://redis:6379/0")
	gpt5_api_key: str = Field(default="")
	gpt5_api_base: str = Field(default="https://api.openai.com/v1")
	cors_origins: List[str] = Field(default_factory=lambda: ["*"])
	aws_s3_bucket: str = Field(default="")
	aws_region: str = Field(default="us-east-1")

	class Config:
		env_file = ".env"
		env_nested_delimiter = "__"