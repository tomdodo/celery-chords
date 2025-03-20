Celery Chords example
=====================

Simple Celery worker task showing the power of Celery Chords.

To run this 
1. Install requirements in new virtualenv in `.venv`
2. Start redis with: `docker compose up -d redis`
3. Start the celery worker with `.venv/bin/python -m celery -A worker.celery worker -l info`

To run a task, from a python console import the task function and use its `delay()` method, for example:

```python
from worker import process_node
process_node.delay()
```
