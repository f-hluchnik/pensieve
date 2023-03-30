import unittest, datetime
from read_messages import get_timestamp

class TestGetTimestamp(unittest.TestCase):

    def timestamp_from_time(self):
        today = datetime.date.today()
        time = datetime.datetime.strptime("23:23", "%H:%M").time()
        dt = datetime.datetime.combine(today, time)
        return dt.timestamp()
    
    def test_get_timestamp(self):
        test_dates = [{"date_string": "23. 09. 2023 23:23", "timestamp": "1695504180"},
                       {"date_string": "23.09.2023 23:23", "timestamp" : "1695504180"},
                       {"date_string": "23. 09. 2023", "timestamp": "1695420000"},
                       {"date_string": "23.09.2023", "timestamp": "1695420000"},
                       {"date_string": "23:23", "timestamp": self.timestamp_from_time()},
                       {"date_string": "wrong", "timestamp": 0}]
        for test_date in test_dates:
            self.assertAlmostEqual(float(get_timestamp(test_date["date_string"])), float(test_date["timestamp"]), delta=1)

if __name__ == '__main__':
    unittest.main()