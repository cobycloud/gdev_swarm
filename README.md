# barfi_swarm

## Scalable Architecture
- Frontend App
	This handles account, billing, and hosting graph editor app

- Frontend Graph Editor App
	This is the magic maker. Enables graph editing operations.

- Backend CRUD API
	Handles communications to and from Sqlite3 db
	
- Redis
	Stores cookies and other KVs

- Backend Distributed Task Queue
	Celery Task Queue to enable execution of everyone's graphs

- Backend Workers
	Agnostic Celery Workers that can process graph tasks

## 