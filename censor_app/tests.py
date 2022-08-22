from django.test import TestCase

from censor_app.views import censor_filter

class Tests(TestCase):
    def test_filter(self):
        result = censor_filter("Привет сучара", "fast")[0]
        self.assertEqual(result, "Привет ******")

        result = censor_filter("м о з г о е б", "deep")[0]
        self.assertEqual(result, "м о з г о ***")

        result = censor_filter("Не пили сук, подстрахуйся", "deep")[0]
        self.assertEqual(result, "Не пили сук, подстрахуйся")