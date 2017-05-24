import sys
from flask import Flask, render_template
from flask import request, _app_ctx_stack
from flask_script import Manager
from script.crawler import Crawler
from script.nlp_worker import NLPWorker
from script.context_worker import ContextWorker
import module.database as db
from module.finder import Finder

app = Flask(__name__)
manager = Manager(app)


@app.route('/')
def root():
    return render_template('search.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('q')
    if query != None:
        res = Finder.search(query)
    else:
        res = ""
    print(res)
    # TODO : do some configuration and make the result clear.
    return render_template('result.html', data=str(res))

@app.teardown_appcontext
def close_app(exception):
    db.close_connection()

@manager.command
def crawler():
    Crawler.load()

@manager.command
def nlp_worker():
    NLPWorker.work()

@manager.command
def context_worker():
    ContextWorker.work()

if __name__ == '__main__':
    print(len(sys.argv))
    if len(sys.argv) == 1:
        app.run(host='0.0.0.0', port=10080)
    else:
        manager.run()
