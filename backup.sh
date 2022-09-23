#!/bin/sh

FILE=dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql
OUTPUT_FILE=${BACKUP_DIR}/${FILE}

mkdir -p ${BACKUP_DIR}

ssh -o StrictHostKeyChecking=no -o ExitOnForwardFailure=yes -f -L 1111:localhost:${DB_PORT} ${SSH_USERNAME}@${SSH_HOST} sleep 10
PGPASSWORD=${SSH_DB_PASSWORD} pg_dump -c -h localhost --port 1111 -U ${DB_USER} ${DB_NAME} -F p -f ${OUTPUT_FILE}

gzip $OUTPUT_FILE

echo "${OUTPUT_FILE}.gz was created:"
ls -l ${OUTPUT_FILE}.gz

find $BACKUP_DIR -maxdepth 1 -mtime +$DAYS_TO_KEEP -name "*.sql.gz" -exec rm -rf '{}' ';'
