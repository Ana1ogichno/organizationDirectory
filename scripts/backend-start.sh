#!/usr/bin/env bash

python3 ./scripts/connection.py

alembic upgrade head

python3 scripts/initializer.py

python3 run.py