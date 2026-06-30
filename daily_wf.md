## 1. Start PostgreSQL (manually)
pg_ctl -D /usr/local/var/postgres start
LC_ALL="en_US.UTF-8" /opt/homebrew/opt/postgresql@18/bin/postgres -D /opt/homebrew/var/postgresql@18

## 2. Activate your venv
cd ~/Semester\ 3/intro-to-db
source venv_db_intro/bin/activate
psql -U "$USER" -d postgres

-- user is Qasim, password is postgres

## 3. Do your work (pgAdmin, psql, Python scripts, etc.)

## 4. When done, deactivate venv and stop Postgres
deactivate
pg_ctl -D /usr/local/var/postgres stop

## 4. How to exit
1. Disconnect from server in pgadmin
2. \q to exit database in psql terminal
3. deactivate to exit virtual environment
4. 


## MongoDB
brew services start mongodb/brew/mongodb-community@8.0
brew services stop mongodb/brew/mongodb-community@8.0