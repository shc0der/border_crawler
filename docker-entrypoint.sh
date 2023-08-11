#!/usr/bin/env bash

alembic upgrade head

python ./app/main.py