#!/bin/bash

source venv/bin/activate
cd factory
./manage.py dumpdata factory auth --exclude=auth.permission --exclude=factory.activity --natural-foreign --indent=2 > factory/fixtures/data.json
deactivate