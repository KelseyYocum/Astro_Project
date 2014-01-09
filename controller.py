from flask import Flask, render_template, redirect, request, g, session, url_for, flash, jsonify
from model import session as DB, User, Series, Episode, Review, UserSeries, requests, pq, add_series
from flask.ext.login import LoginManager, login_required, login_user, current_user
from flaskext.markdown import Markdown
import config
import forms
import model
import json
import operator


app = Flask(__name__)
app.config.from_object(config)

Markdown(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def authenticate():
    form = forms.LoginForm(request.form)
    if not form.validate():
        flash("Incorrect username or password") 
        return render_template("login.html")

    email = form.email.data
    password = form.password.data

    user = User.query.filter_by(email=email).first()

    if not user or not user.authenticate(password):
        flash("Incorrect username or password") 
        return render_template("login.html")

    login_user(user)

    return redirect(request.args.get("next", url_for("index")))

@app.route("/")
def index():
    series = Series.query.all()
    return render_template("index.html")


    


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')