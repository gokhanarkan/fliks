from flask import Flask

app = Flask(__name__)

from views import *
from config import *

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=heroku_port)