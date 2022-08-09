import unittest
import ranking

import sys
import unittest
import logging

logger = logging.getLogger()
logger.level = logging.DEBUG

def p_pass():
    print("pass")
    
class TestRanking(unittest.TestCase):
    def test_split(self):
        print("\nTesting Team_Split\n")
        result = ranking.team_split('Tarantulas 3')
        self.assertEqual(result, ('Tarantulas ', '3'))

    def test_database(self):
        print("\nTesting Database\n")
        result = ranking.update_data_from_db('AllTournaments')
        self.assertIsNotNone(result)

    def test_print_points(self):
        print("\nTesting Print_Points\n")
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)
        try:
            points = [['Tarantulas', 6], ['Lions', 5], ['FC Awesome', 1], ['Snakes', 1], ['Grouches', 0]]
            ranking.print_points(points)
        finally:
            logger.removeHandler(stream_handler)

if __name__ == "__main__":
    unittest.main()