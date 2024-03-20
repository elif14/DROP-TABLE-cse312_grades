# How to print in Flask
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
# Blueprint
## Why should we use Blueprint?
Blueprint is extremely powerful and useful. There are more to Blueprint, but our main purpose is to _encapsulate_ our code/file.
By separating one mega py file to many different py files, we'll be able to organize the code and functionality better.
- Easier to understand
- Easier to maintain
- Less likelihood of merge conflicts
## How to use Blueprint to separate files
1. Create new python file.
```
new.py
```
2. Import Blueprint.
```
from flask import Blueprint
```
3. Add following line at the top of the file.
```
example_bp = Blueprint('example_bp', __name__,
    template_folder='templates',
    static_folder='static')
```
4. Add route and functions like so.
```
@example_bp.route('/baz.bar')
def foo():
    pass
```
5. Register Blueprint
Go to server.py and add following 2 lines.
```
from register.new import example_bp
```
```
app.register_blueprint(example_bp)
```
# Feature
## Part 1
### Objective 1 Hosting a Static Page
- [x] HTML hosted at the root path
- [x] CSS hosted at a separate path
- [x] JavaScript hosted at a separate path
- [x] At least one image
- [ ] All files have correct MIME type
- [ ] X-Content-Type-Options: nosniff header must be set
> [!CAUTION]
> - All of these parts must be hosted by your server.
> - Must serve the image from your server using your framework of choice.
> - App should run on local port 8080

### Objective 2 Authentication
- [x] Home page has a registration form
    - [ ] User can register
    - [x] User should still be on the home page after registration
    - [ ] Registeration confirms password
        - [ ] Verifying second confirmation password is done in server not the frontend
    - [ ] User can not register with a taken username
    - [x] Store user name and hashed password in the database
- [x] Home page has a login form
    - [x] User can login  
    - [x] User should still be on the home page after login
    - [ ] Username must be displayed on the home page after logging in
    - [ ] User can logout
        - [ ] Invalidate their auth token when log out
    - [ ] Set an authentication token as a cookie
        - [x] Must be a random value
        - [ ] Store a **hash** of each token in the database
        - [ ] **HttpOnly** directive set
        - [ ] The auth token cookie must have an expiration time of 1 hour or longer 


### Objective 3 Making Interactive Posts
- [ ]
- [ ]
- [ ]



