#!/bin/bash

source venv/bin/activate
cd factory
./manage.py dumpdata factory auth --exclude=auth.permission --natural-foreign --indent=2 > factory/fixtures/data.json
deactivate