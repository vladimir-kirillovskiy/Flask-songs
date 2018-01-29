from main import app
import unittest
import json

class FlaskTestCase(unittest.TestCase):

    def test_index_status(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_songs_status(self):
        tester = app.test_client(self)
        response = tester.get('/songs', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_avg_difficulty_status(self):
        tester = app.test_client(self)
        response = tester.get('/songs/avg/difficulty', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_song_search_status(self):
        tester = app.test_client(self)
        response = tester.get('/songs/search', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    # def test_song_rating_status(self):
    #     tester = app.test_client(self)
    #     response = tester.get('/songs/rating', content_type='application/json')
    #     self.assertEqual(response.status_code, 200)

    def test_get_song_rating_status(self):
        tester = app.test_client(self)
        response = tester.get('/songs/avg/rating/<song_id>', content_type='application/json')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()