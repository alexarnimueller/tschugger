#!/bin/sh

now=$(date +"%Y-%m-%d")
pg_dump -w -U tschugger -d tschugger > "/backups/db_backup_$now.sql"

# remove all files (type f) modified longer than 180 days ago under /backups
find /backups -name "*.sql" -type f -mtime +365 -delete

exit 0
