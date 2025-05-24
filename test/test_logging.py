import unittest
import os
from comp.logging.Logger import Logger

class Test_LogSuite(unittest.TestCase):
    
    def setUp(self):
        self._path_name = os.path.abspath(__file__) + "test.log"
        self._logger = Logger(self._path_name).logger

    def test_log_message(self):
        self._logger.info("This is a test message")
        with open(self._path_name, "r") as file:
            row = file.read()
            print(row)
            self.assertEqual(row.split("-")[-1].strip(" \n"), "This is a test message") 
            
if __name__ == '__main__':
    unittest.main()