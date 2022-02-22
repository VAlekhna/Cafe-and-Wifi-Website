from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SECRET_KEY'] = 'RanDomKey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db = SQLAlchemy(app)

Bootstrap(app)


# Cafe TABLE Configuration


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=True)
    coffee_price = db.Column(db.String(250), nullable=True)


# db.create_all()


class CafeForm(FlaskForm):
    name = StringField("Cafe name", validators=[DataRequired()])
    map_url = StringField("Cafe location on Google maps (URL)", validators=[DataRequired(), URL()])
    img_url = StringField("Cafe image (URL)", validators=[DataRequired(), URL()])
    location = StringField("Cafe location (Area)", validators=[DataRequired()])
    has_sockets = SelectField("Power Socket Availability", choices=["Yes", "No"], validators=[DataRequired()])
    has_toilet = SelectField("Toilets Available?", choices=["Yes", "No"], validators=[DataRequired()])
    has_wifi = SelectField("Wifi Available?", choices=["Yes", "No"], validators=[DataRequired()])
    can_take_calls = SelectField("Call taking Available?", choices=["Yes", "No"], validators=[DataRequired()])
    seats = SelectField("How many seats?", choices=["0-10", "10-20", "20-30", "30-40", "50+"])
    coffee_price = StringField("Coffee price", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        if form.validate_on_submit():

            if form.has_sockets.data == "Yes":
                sockets_yn = 1
            else:
                sockets_yn = 0

            if form.has_sockets.data == "Yes":
                toilet_yn = 1
            else:
                toilet_yn = 0

            if form.has_sockets.data == "Yes":
                wifi_yn = 1
            else:
                wifi_yn = 0

            if form.has_sockets.data == "Yes":
                calls_yn = 1
            else:
                calls_yn = 0

        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            has_sockets=sockets_yn,
            has_toilet=toilet_yn,
            has_wifi=wifi_yn,
            can_take_calls=calls_yn,
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("cafes"))
    return render_template("add_cafe.html", form=form)


@app.route('/cafes')
def cafes():
    all_cafes = Cafe.query.all()
    return render_template("cafes.html", all_cafes=all_cafes)


@app.route('/edit-cafe/<int:cafe_id>', methods=["GET", "POST"])
def edit(cafe_id):
    cafe = Cafe.query.get(cafe_id)

    if cafe.has_sockets == 1:
        sockets_yn = "Yes"
    else:
        sockets_yn = "No"

    if cafe.has_toilet == 1:
        toilet_yn = "Yes"
    else:
        toilet_yn = "No"

    if cafe.has_wifi == 1:
        wifi_yn = "Yes"
    else:
        wifi_yn = "No"

    if cafe.can_take_calls == 1:
        calls_yn = "Yes"
    else:
        calls_yn = "No"

    edit_form = CafeForm(
        name=cafe.name,
        map_url=cafe.map_url,
        img_url=cafe.img_url,
        location=cafe.location,
        has_sockets=sockets_yn,
        has_toilet=toilet_yn,
        has_wifi=wifi_yn,
        can_take_calls=calls_yn,
        seats=cafe.seats,
        coffee_price=cafe.coffee_price
    )
    if edit_form.validate_on_submit():

        if edit_form.has_sockets.data == "Yes":
            sockets_yn = 1
        else:
            sockets_yn = 0

        if edit_form.has_toilet.data == "Yes":
            toilet_yn = 1
        else:
            toilet_yn = 0

        if edit_form.has_wifi.data == "Yes":
            wifi_yn = 1
        else:
            wifi_yn = 0

        if edit_form.can_take_calls.data == "Yes":
            calls_yn = 1
        else:
            calls_yn = 0

        cafe.name = edit_form.name.data
        cafe.map_url = edit_form.map_url.data
        cafe.img_url = edit_form.img_url.data
        cafe.location = edit_form.location.data
        cafe.has_sockets = sockets_yn
        cafe.has_toilet = toilet_yn
        cafe.has_wifi = wifi_yn
        cafe.can_take_calls = calls_yn
        cafe.seats = edit_form.seats.data
        cafe.coffee_price = edit_form.coffee_price.data

        db.session.commit()
        return redirect(url_for('cafes'))
    return render_template('add_cafe.html', form=edit_form, is_edit=True)


@app.route('/delete')
def delete_page():
    all_cafes = Cafe.query.all()
    return render_template('delete.html', cafes=all_cafes)


@app.route('/delete/<int:cafe_id>')
def delete(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('delete_page'))


if __name__ == '__main__':
    app.run()
