#!/bin/sh
set -e

# Run database migrations
echo "Running database migrations..."
python -m alembic upgrade head

# Execute the main command
echo "Starting application..."
exec "$@"