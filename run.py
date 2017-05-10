import sys
from flask import Flask, render_template
from flask import request, _app_ctx_stack
from flask_script import Manager
from script.crawler import Crawler

app = Flask(__name__)
manager = Manager(app)


@app.route('/')
def root():
    return render_template('search.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('q')
    return query

@app.teardown_appcontext
def close_connection(exception):
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()

@manager.command
def hello():
    Crawler.load()

if __name__ == '__main__':
    print(len(sys.argv))
    if len(sys.argv) == 1:
        app.run(host='0.0.0.0', port=10080)
    else:
        manager.run()
