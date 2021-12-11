import unittest 
from utils import * 

class TestTimeConversion(unittest.TestCase):

    def test_time_conversion(self):
        res = convert_to_datetime("5am")
        self.assertEqual(time.strftime("%H:%M:%S", res), '05:00:00')
        res = convert_to_datetime("6.59pm")
        self.assertEqual(time.strftime("%H:%M:%S", res), '18:59:00')
        print(type(res))

class TestRegex(unittest.TestCase):

    def test_match_sentence_pattern(self):
        txt = "7am-10pm"
        x = re.search("^[0-9]+(am|pm).*[0-9]+(am|pm)(?:.+)?", txt)
        self.assertTrue(x)


    def test_split_sentences(self):
        #https://stackoverflow.com/questions/55083483/split-sentences-based-on-different-patterns-in-python-3
        texts = [
            ' 7am-10.59am: $4.80 per entry. 11am-7.59pm: $2.50 per hr. 8pm-6.59am: $0.05/min.',
            '7am-1pm: $3 for 1st hr, $1.50 for sub 30 mins. 1pm-11pm: $3 for 1st 2 hr, $1.00 for sub 30 mins. 11pm-7am: $15 per entry.',
            '$3.75 per entry Concorde Hotel', 
            '7am-7.59pm: $3 for 1st hr, $1.50 for sub 30mins.',
            '7am-10.59am/2pm-4.59pm: $2.50 for 1st hr or part thereof, $1.20 for sub 30 mins; 11am-1.59pm: $3.00 for 1st hr or part thereof, $1.50 for sub 30 mins',

        ]
        number_of_sentences = [3, 3, 1, 1, 2]
        for text, ans in zip(texts, number_of_sentences):
            lines = split_lines(text)
            print(lines)
            self.assertEqual(len(lines), ans, f"wrong {lines}")
        
        print('#'*100)

    def test_find_numeric_inputs(self):
        texts = ['7am-10.59am: $4.80 per entry.', 
                '7am-1pm: $3 for 1st hr; $1.50 for sub 30 mins.',
                '8pm-6.59am: $4/entry.'
        ]
        answers = [3, 6, 3]
        for text, ans in zip(texts, answers):
            numeric = find_numerical_inputs(text)
            self.assertEqual(len(numeric), ans)
            print(numeric)
        print('#'*100)
        

if __name__ == '__main__':
    unittest.main()