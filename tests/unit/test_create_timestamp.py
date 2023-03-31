import unittest, datetime
from read_messages import create_timestamp

class TestCreateTimestamp(unittest.TestCase):

    def timestamp_from_time(self):
        today = datetime.date.today()
        time = datetime.datetime.strptime("23:23", "%H:%M").time()
        dt = datetime.datetime.combine(today, time)
        return dt.timestamp()
    
    def test_create_timestamp_valid(self):
        test_dates = [{"date_string": "23. 09. 2023 23:23", "timestamp": "1695504180"},
                       {"date_string": "23.09.2023 23:23", "timestamp" : "1695504180"},
                       {"date_string": "23. 09. 2023", "timestamp": "1695420000"},
                       {"date_string": "23.09.2023", "timestamp": "1695420000"},
                       {"date_string": "23:23", "timestamp": self.timestamp_from_time()}]
        for test_date in test_dates:
            self.assertAlmostEqual(float(create_timestamp(test_date["date_string"])), float(test_date["timestamp"]), delta=1)
    
    def test_create_timestamp_invalid(self):
        test_dates = [{"date_string": "wrong"},
                      {"date_string": "123:20"}]
        for test_date in test_dates:
            self.assertIsNone(create_timestamp(test_date["date_string"]))

if __name__ == '__main__':
    unittest.main()