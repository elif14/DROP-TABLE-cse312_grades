# https://flask.palletsprojects.com/en/2.3.x/blueprints/
# https://realpython.com/flask-blueprint/
# Here are resources on how to use Blueprint in Flask

from flask import Flask

from register.register import register_bp

app = Flask(__name__)

#app.register_blueprint(register_bp, url_prefix='/')
app.register_blueprint(register_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
