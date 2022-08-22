from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
import os

# TODO: create images, replace placeholders

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
