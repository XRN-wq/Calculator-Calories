from flask import Flask, render_template, request
import math
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Dates(Base):
    __tablename__ = "Dates"
    id = Column(Integer, primary_key=True)
    date_time = Column(String)


class Calories(Base):
    __tablename__ = "Calories"
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    category = Column(String)
    item = Column(String)
    gramms = Column(String)
    date_id = Column(Integer)


def db_connection():
    try:
        engine = create_engine("postgresql://postgres:steampank228@localhost/db")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
    except Exception as e:
        print("Ошибка подключения к серверу:", e)


app = Flask(__name__, template_folder="template")

app.debug = True


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session = db_connection()
        date_time = request.form["date"]
        calories = request.form["calories"]
        category = request.form["category"]
        item = request.form["item"]
        gramms = request.form["amount"]
        if gramms == "":
            gramms = "-"
        else:
            gramms = str(gramms)
        if category is None:
            category = "-"
        if item is None:
            item = "-"
        existing_date = session.query(Dates).filter_by(date_time=date_time).first()
        if existing_date is None:
            new_date = Dates(date_time=date_time)
            existing_date = new_date
            session.add(new_date)
            session.flush()
        else:
            pass

        new_calories = Calories(
            date_id=existing_date.id, amount=calories, category=category, item=item, gramms=gramms
        )
        session.add(new_calories)
        session.commit()

    return render_template("index.html")


@app.route("/statistics", methods=["GET", "POST"])
def statistics():
    session = db_connection()
    calories = session.query(Calories).all()
    dates = session.query(Dates).all()
    dates_not_empty = []

    for date in dates:
        for calorie in calories:
            if calorie.date_id == date.id:
                dates_not_empty.append(date)
    dates_not_empty = list(set(dates_not_empty))
    total_calories = sum([calorie.amount for calorie in calories])
    average_calories = total_calories / len(dates_not_empty) if len(dates_not_empty) > 0 else 0
    average_calories = round(average_calories)
    if request.method == "POST":
        delete_id = request.form["delete"]
        calorie = session.query(Calories).filter_by(id=delete_id).first()

        if calorie is not None:
            session.delete(calorie)
            session.commit()

            calories = [c for c in calories if c.id != int(delete_id)]
            dates_not_empty = []
            for date in dates:
                for calorie in calories:

                    if calorie.date_id == date.id:
                        dates_not_empty.append(date)
            dates_not_empty = list(set(dates_not_empty))
            total_calories = sum([c.amount for c in calories])
            average_calories = total_calories / len(dates_not_empty) if len(dates_not_empty) > 0 else 0
            average_calories = round(average_calories)
    dates_not_empty.sort(key=lambda x: x.date_time, reverse=True)
    return render_template(
        "statistics.html",
        dates=dates_not_empty,
        calories=calories,
        average_calories=average_calories
    )


if __name__ == "__main__":
    app.run()
