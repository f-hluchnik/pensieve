import unittest, datetime
from read_messages import format_thought

class TestFormatThought(unittest.TestCase):
    
    def test_format_thought(self):
        test_messages = [
            {
            "message": {"text": "This is the text of a message containing hashtags and time. (@ 21. 10. 2023 11:55) #life #fun", "ts": "1647267240"},
            "expected_thought": {'text': "This is the text of a message containing hashtags and time.", 'timestamp_print': "1697882100.0", 'timestamp_real': "1647267240", 'hashtags': ["#life", "#fun"]}
            },
            {
            "message": {"text": "This is the text of a message containing no hashtags and time. (@ 21. 10. 2023 11:55)", "ts": "1647267240"},
            "expected_thought": {'text': "This is the text of a message containing no hashtags and time.", 'timestamp_print': "1697882100.0", 'timestamp_real': "1647267240", 'hashtags': []}
            },
            {
            "message": {"text": "This is the text of a message containing no hashtags and no time.", "ts": "1647267240"},
            "expected_thought": {'text': "This is the text of a message containing no hashtags and no time.", 'timestamp_print': "1647267240", 'timestamp_real': "1647267240", 'hashtags': []}
            },
        ]
        for test_message in test_messages:
            thought = format_thought(test_message["message"])
            self.assertEqual(thought, test_message["expected_thought"])

if __name__ == '__main__':
    unittest.main()