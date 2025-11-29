import os
import redis
from rq import Queue

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

_redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
job_queue = Queue("matches", connection=_redis_conn)


def enqueue_match_processing(match_id: int) -> str:
    """
    Enqueue a match processing job.

    The worker exposes: worker.main.process_match
    """
    job = job_queue.enqueue("worker.main.process_match", match_id)
    return job.id