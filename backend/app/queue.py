from flask import current_app, g
from redis import Redis
from rq import Queue

def get_queue():
    if 'queue' not in g:
        redis = Redis.from_url(current_app.config['REDIS_URL'])
        g.queue = Queue("creatorflow", connection=redis)
    return g.queue
