from flask_jwt_extended import JWTManager
from pymongo import MongoClient
import redis as redis_lib
from rq import Queue
from apscheduler.schedulers.background import BackgroundScheduler
import structlog


class MongoWrapper:
	client: MongoClient | None = None
	def init_app(self, uri: str):
		self.client = MongoClient(uri)
	def get_db(self, name: str = "creatorflow"):
		assert self.client is not None, "Mongo client not initialized"
		return self.client[name]


class RedisWrapper:
	client: redis_lib.Redis | None = None
	def init_app(self, url: str):
		self.client = redis_lib.from_url(url)


class RQWrapper:
	queue: Queue | None = None
	def init_app(self, redis_client: redis_lib.Redis):
		self.queue = Queue("creatorflow-queue", connection=redis_client)
	def enqueue(self, *args, **kwargs):
		assert self.queue is not None
		return self.queue.enqueue(*args, **kwargs)


class SchedulerWrapper:
	scheduler: BackgroundScheduler | None = None
	def init_app(self, app):
		self.scheduler = BackgroundScheduler(timezone="UTC")
		self.scheduler.start()


jwt = JWTManager()
mongo_client = MongoWrapper()
redis_client = RedisWrapper()
rq_queue = RQWrapper()
scheduler = SchedulerWrapper()
logger = structlog.get_logger("creatorflow")