from flask import Flask, render_template
from flask import request

app = Flask(__name__)


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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10080)
