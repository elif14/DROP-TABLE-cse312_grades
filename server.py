from flask import Flask
from logging.config import dictConfig 

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

from LineUp.homepage import homepage_bp
from LineUp.register import register_bp
from LineUp.login import login_bp
from LineUp.ta import ta_bp

app = Flask(__name__)

app.register_blueprint(homepage_bp)
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(ta_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
