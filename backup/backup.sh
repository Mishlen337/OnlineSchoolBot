#!/bin/sh

FILE=dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql
OUTPUT_FILE=${BACKUP_DIR}/${FILE}

mkdir -p ${BACKUP_DIR}

ssh -o StrictHostKeyChecking=no -o ExitOnForwardFailure=yes -f -L 1111:localhost:${SSH_POSTGRES_PORT} ${SSH_USERNAME}@${SSH_HOST} sleep 10
PGPASSWORD=${SSH_POSTGRES_PASSWORD} pg_dump -c -h localhost --port 1111 -U ${SSH_POSTGRES_USER} -d ${SSH_POSTGRES_DB} -F p -f ${OUTPUT_FILE}

gzip $OUTPUT_FILE

echo "${OUTPUT_FILE}.gz was created:"
ls -l ${OUTPUT_FILE}.gz

find $BACKUP_DIR -maxdepth 1 -mtime +$DAYS_TO_KEEP -name "*.sql.gz" -exec rm -rf '{}' ';'
