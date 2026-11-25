import unittest

from tidecast.app import route


class RouteTest(unittest.TestCase):
    def test_stations(self):
        status, body = route("/stations")
        self.assertEqual(status, 200)
        self.assertEqual({s["id"] for s in body}, {"9414290", "8518750", "9447130"})

    def test_tides(self):
        status, body = route("/stations/9414290/tides")
        self.assertEqual(status, 200)
        self.assertEqual(len(body), 120)

    def test_unknown(self):
        self.assertEqual(route("/stations/1/tides")[0], 404)
        self.assertEqual(route("/nope")[0], 404)


if __name__ == "__main__":
    unittest.main()
