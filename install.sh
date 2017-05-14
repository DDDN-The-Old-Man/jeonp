mkdir -p /home/www/jp/
cp * /home/www/jp/
cd /home/www/jp/
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
. mecab.sh
export FLASK_APP=run.py
