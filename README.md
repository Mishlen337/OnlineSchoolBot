To start the project, you need:
1) create and fill in .env file (virtual variable names maintain in .env_example)
2) docker-compose build
3) docker-compose up -d

To tune backup cron, you need:
1) ssh-keygen
2) cat ~/.ssh/id_rsa.pub | ssh root@[ip_address] 'cat >> ~/.ssh/authorized_keys'
3) sudo apt-get install postgresql-client
4) sudo apt install postgresql postgresql-contrib
5) sudo systemctl start postgresql.service
4) chmod u+x [dir path]/backup/backup.sh
5) crontab -e
6) fill file coping data from [dir path]/backup/cronjobs
