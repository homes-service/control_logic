#!/bin/bash
alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 9000 --reload