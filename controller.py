from flask import Flask, render_template, redirect, request, g, session, url_for, flash, jsonify
from model import session as DB, User
from flask.ext.login import LoginManager, login_required, login_user, current_user
from flaskext.markdown import Markdown
from pygeocoder import Geocoder
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
    location_obj_list = DB.query(model.Location).all()
    locations = []
    for location in location_obj_list:
        location_id = location.id
        lat = location.lat
        lng = location.lng
        description = location.description
        name = location.name
        locations.append({"id":location_id, "lat":lat, "lng":lng, "description":description, "name":name})
    locations = json.dumps(locations)
    print locations
    return render_template("index.html", locations=locations, location_obj_list=location_obj_list)





if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')