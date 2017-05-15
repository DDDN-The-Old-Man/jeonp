virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
. script/mecab.sh
export FLASK_APP=run.py
sqlite3 database.db < script/dbschema.sql
