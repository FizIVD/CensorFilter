from django.test import TestCase

from censor_app.views import censor_filter, MethodType


class Tests(TestCase):
    def test_filter(self):
        result = censor_filter("Привет сучара", MethodType.fast)[0]
        self.assertEqual(result, "Привет ******")

        result = censor_filter("м о з г о е б", MethodType.deep)[0]
        self.assertEqual(result, "м о з г *****")

        result = censor_filter("Не пили сук, подстрахуйся", MethodType.deep)[0]
        self.assertEqual(result, "Не пили сук, подстрахуйся")
