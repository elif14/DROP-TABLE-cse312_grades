# How to print
Normal print() **does not** work in flask.
Using standard error or flush in print() also **does not** work.
```
print('Hello world!', file=sys.stderr)
print('Hello world!', flush=True)
```
Only reliable method I was able to find is using [logger](https://flask.palletsprojects.com/en/2.3.x/logging/).
```
import logging
from flask import Flask

app = Flask(__name__)

@app.route('/print')
def printMsg():
    app.logger.warning('testing warning log')
    app.logger.error('testing error log')
    app.logger.info('testing info log')
    return "Check your console"
```
However, since we are using [Blueprint](https://flask.palletsprojects.com/en/2.3.x/blueprints/) to organize different files and functionalities, we need to use small twist to this method by importing [current_app](https://stackoverflow.com/questions/16994174/in-flask-how-to-access-app-logger-within-blueprint).
```
from flask import current_app
current_app.logger.info('Hello world!')
```
