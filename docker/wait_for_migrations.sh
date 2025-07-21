#!/bin/bash

echo "⏳ Migrations not yet applied. Waiting..."
until python manage.py showmigrations | grep '\[X\]' > /dev/null; do
  sleep 1
done
echo "✅ Migrations applied. Continuing..."