import unittest
from script import app, db_connection, Dates, Calories
import datetime

class TestApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.session = db_connection()

    def tearDown(self):
        self.session.rollback()

    def test_index_post(self):
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        calories = 500
        category = "meat"
        item = "Курица"
        gramms = "100"

        response = self.app.post("/", data={
            "date": date_time,
            "calories": calories,
            "category": category,
            "item": item,
            "amount": gramms
        })

        self.assertEqual(response.status_code, 200)

        existing_date = self.session.query(Dates).filter_by(date_time=date_time).first()
        self.assertIsNotNone(existing_date)

        existing_calories = self.session.query(Calories).filter_by(date_id=existing_date.id).first()
        self.assertIsNotNone(existing_calories)

        self.assertEqual(existing_calories.amount, calories)
        self.assertEqual(existing_calories.category, category)
        self.assertEqual(existing_calories.item, item)
        self.assertEqual(existing_calories.gramms, gramms)

    def test_index_get(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Index</title>", response.data)

    def test_statistics_get(self):
        response = self.app.get("/statistics")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Statistics</title>", response.data)


if __name__ == "__main__":
    unittest.main()
