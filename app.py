from flask import Flask, request, render_template, redirect
from flask_sslify import SSLify
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
from uuid import uuid4
from werkzeug.contrib.fixers import ProxyFix
from os import getenv

db = TinyDB(storage=MemoryStorage)
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
sslify = SSLify(app, skips=['health'], age=300, permanent=True)

app.debug = getenv('DEBUG', False)
app.config['theme'] = getenv('THEME', 'light')


@app.route('/', methods=['GET', 'POST'])
def default():
    if request.method == 'POST':
        return render_template('index.html', error=True)
    else:
        return render_template('index.html')


@app.route('/create/', methods=['POST'])
def create():
    key = uuid4().hex
    secret = request.form['secret'].encode('utf-8')
    if not secret:
        return redirect('/', 307)
    else:
        db.insert({'key': key, 'secret': secret})
        secret_url = request.url_root + 'get/' + key

        return render_template('create.html', url=secret_url)


@app.after_request
def add_header(r):
    r.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    r.headers['Pragma'] = 'no-cache'
    r.headers['Expires'] = '0'
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/get/<key>')
def retrieve(key=None):
    try:
        result = db.search(Query().key == key)[0]
        secret = result['secret'].decode('utf-8')
        # set secret to an empty string
        db.update({'secret': ''.encode('utf-8')}, Query().key == key)
    except:
        secret = False

    return render_template('get.html', secret=secret)


@app.route('/health', methods=['GET'])
def health():
    return 'OK'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
