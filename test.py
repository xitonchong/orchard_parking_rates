import unittest 
from utils import * 

class TestTimeConversion(unittest.TestCase):

    def test_time_conversion(self):
        res = convert_to_datetime("5am")
        self.assertEqual(time.strftime("%H:%M:%S", res), '05:00:00')

        

if __name__ == '__main__':
    unittest.main()