from flask import Flask, render_template, request, render_template_string, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import datetime
import random

from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBAasdjbf2oi4397C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eatlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
week_menu = [None] * 7


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meal = db.Column(db.String(80))
    complex = db.Column(db.Boolean, default=False)
    last_used = db.Column(db.Date)


def init_db():
    try:
        f = open('eatlist.db')
    except IOError:
        menu = []
        db.create_all()
        eetlijst = open('eetlijst.txt', 'r')
        for line in eetlijst.readlines():
            menu_item = line.strip()
            if len(menu_item) != 0:
                if not menu_item in menu:
                    menu.append(menu_item)
                    new_meal = Meal(
                        meal=menu_item,
                        complex=0,
                        last_used=datetime.datetime.now()
                    )
                    db.session.add(new_meal)
                    db.session.commit()


def get_meals():
    # search_date = datetime.datetime.now()-datetime.timedelta(14)
    easy_meals = db.session.query(Meal).filter().filter_by(complex=0).all()
    complex_meals = db.session.query(Meal).filter().filter_by(complex=1).all()
    # print(len(easy_meals + complex_meals))
    # if not len(easy_meals + complex_meals) == 21:
    #     easy_meals = db.session.query(Meal).filter(Meal.last_used >= func.DATE(search_date)).filter_by(complex=0).all()
    #     complex_meals = db.session.query(Meal).filter(Meal.last_used >= func.DATE(search_date)).filter_by(
    #         complex=1).all()

    menu_items = []
    while len(menu_items) < 7:
        if len(menu_items) < 2:
            new_item = random.choice(complex_meals)
        else:
            new_item = random.choice(easy_meals)
        if new_item.meal not in menu_items:
            menu_items.append([new_item.meal, new_item.id])
            eat = db.session.query(Meal).filter_by(meal=new_item.meal).first()
            eat.last_used = func.DATE(datetime.datetime.utcnow())
            db.session.commit()

    return menu_items


def get_menu():
    return week_menu


def add_to_menu(day: int, meal_id: int, meal_name: str):
    week_menu[day - 1] = [meal_name, meal_id]


@app.route("/")
def home():
    return render_template("index.html", meals=get_meals(), menu=get_menu())


@app.route("/select_meal", methods=['POST', 'GET'])
def select_meal():
    if request.method == 'GET':
        return redirect(url_for('home'))
    if request.method == 'POST':
        form_data = request.form
        add_to_menu(int(form_data['day']), int(form_data['meal-id']), form_data['meal-name'])
        return redirect(url_for('home'))
    return redirect(url_for('home'))


@app.route("/reset_menu")
def reset_menu():
    global week_menu
    week_menu = [None] * 7
    return render_template("index.html", meals=get_meals(), menu=get_menu())


if __name__ == '__main__':
    init_db()
    app.run(host='10.0.0.103')
