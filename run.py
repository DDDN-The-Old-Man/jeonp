import sys
from flask import Flask, render_template
from flask import request, _app_ctx_stack
from flask_script import Manager
from script.crawler import Crawler
from script.nlp_worker import NLPWorker
from script.context_worker import ContextWorker
import module.database as db
from module.finder import Finder
from module.simsen import SimSen
from module.nlp_parser import NLPParser
import json

app = Flask(__name__)
manager = Manager(app)


@app.route('/')
def root():
    return render_template('search.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        query = request.args.get('q', '')
    else:
        query = request.form.get('q')
    if query != None:
        res = Finder.search(query)
    else:
        res = "{}"
    # TODO : do some configuration and make the result clear.
    if request.method == 'GET':
        return res
    ret = json.loads(res)

    return render_template('result.html', results=ret, q=query)

@app.route('/sentence_sim', methods=['GET', 'POST'])
def sentence_sim():
    if request.method == 'GET':
        sen1 = request.args.get('sen1', '')
        sen2 = request.args.get('sen2', '')
    else:
        sen1 = request.form.get('sen1', '')
        sen2 = request.form.get('sen2', '')

    q1 = NLPParser.parse(sen1)
    q2 = NLPParser.parse(sen2)
    result = {
            'sen1': sen1,
            'sen2': sen2,
            'parsed_sen1': q1,
            'parsed_sen2': q2,
            'similarity': SimSen.similarity(q1, q2)
            }
    return json.dumps(result)


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
