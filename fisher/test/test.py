from flask import Flask, current_app

app = Flask(__name__)
# ctx = app.app_context()
# ctx.push()
# a = current_app
# b = a.config['DEBUG']
with app.app_context():
    a = current_app
    b = a