from typing import Optional

from celery import Celery, Task
from redis import Redis

REDIS_URL = "redis://127.0.0.1:6379"
CELERY_BROKER_REDIS_DATABASE = 1
CELERY_RESULTS_REDIS_DATABASE = 2

celery = Celery(
    __name__,
    broker=f"{REDIS_URL}/{CELERY_BROKER_REDIS_DATABASE}",
    result_backend=f"{REDIS_URL}/{CELERY_RESULTS_REDIS_DATABASE}",
)
redis = Redis.from_url(REDIS_URL, decode_responses=True)

ROOT = "root"
TREE = {
    ROOT: {
        "branches": ["A", "B"],
        "users": list(range(0, 19)),
    },
    "A": {
        "branches": ["C", "D", "E"],
        "users": [2, 4],
    },
    "B": {
        "branches": ["F", "G"],
        "users": [6, 7],
    },
    "C": {
        "branches": [],
        "users": [8, 9, 10],
    },
    "D": {
        "branches": [],
        "users": [17, 18],
    },
    "E": {
        "branches": [],
        "users": [11, 12],
    },
    "F": {
        "branches": [],
        "users": [13, 14],
    },
    "G": {
        "branches": [],
        "users": [15, 16],
    },
}
VISITED_USERS_SET_NAME = "visited-users"


@celery.task(name="process_node", ignore_result=False, bind=True)
def process_node(self: Task, node_id: Optional[str] = None) -> None:
    print(f"*** Task {self.name} - processing branch {node_id}")

    node_id = node_id or ROOT
    if node_id == ROOT:
        redis.delete(VISITED_USERS_SET_NAME)

    users = TREE[node_id]["users"]
    if node_id != ROOT:
        redis.sadd(VISITED_USERS_SET_NAME, *users)
        print(f"\t- Processed users: {users}")

    for branch_id in TREE[node_id]["branches"]:
        process_node.delay(branch_id)

    visited_nodes = [int(i) for i in redis.smembers(VISITED_USERS_SET_NAME)]
    print(f"\t- visited nodes: {sorted(visited_nodes)}")
