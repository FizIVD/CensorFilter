from django.test import TestCase
from .new_censor import new_censor_filter

class NewCensorTests(TestCase):

    def test_simple_profanity(self):
        self.assertEqual(new_censor_filter("Привет, хуй"), "Привет, ***")
        self.assertEqual(new_censor_filter("Это просто пиздец"), "Это просто ******")
        self.assertEqual(new_censor_filter("Ну ты и сука"), "Ну ты и ****")

    def test_transliteration(self):
        self.assertEqual(new_censor_filter("privet, xuy"), "privet, ***")
        self.assertEqual(new_censor_filter("eto prosto p1zdets"), "eto prosto *******")
        self.assertEqual(new_censor_filter("nu ti i s-u-k-a"), "nu ti i *******")

    def test_character_duplication(self):
        self.assertEqual(new_censor_filter("сууууука"), "********")
        self.assertEqual(new_censor_filter("бббллляяяя"), "**********")
        self.assertEqual(new_censor_filter("пиздееееец"), "**********")

    def test_separators(self):
        # Note: 'б л я' is now tested in mixed_cases as the logic has changed
        self.assertEqual(new_censor_filter("п-и-з-д-а"), "*********")
        self.assertEqual(new_censor_filter("х.у.й"), "*****")

    def test_mixed_cases(self):
        self.assertEqual(new_censor_filter("3.14здец"), "********") # leetspeak + separator
        # Test changed as per user agreement for split-and-check logic
        self.assertEqual(new_censor_filter("cyka blyat"), "**** *****") # translit
        self.assertEqual(new_censor_filter("F U C K"), "* * * *") # english with separators
        self.assertEqual(new_censor_filter("p-i-d-o-r"), "*********") # translit + separators
        self.assertEqual(new_censor_filter("б л я"), "* * *")

    def test_misspellings_and_variations(self):
        # Note: The effectiveness of this depends on the roots in BadPartsOfWords.txt
        # 'пидр' and 'пидар' are common variations of 'пидор'
        self.assertEqual(new_censor_filter("ты пидр"), "ты ****")
        self.assertEqual(new_censor_filter("он пидар"), "он *****")
        # 'ебл' is a root for many swear words
        self.assertEqual(new_censor_filter("ебливый"), "*******")

    def test_false_positives(self):
        self.assertEqual(new_censor_filter("командный дух"), "командный дух")
        self.assertEqual(new_censor_filter("херес это вино"), "херес это вино")
        self.assertEqual(new_censor_filter("страховка на машину"), "страховка на машину")
        self.assertEqual(new_censor_filter("купить сукно"), "купить сукно")
        self.assertEqual(new_censor_filter("лебединая песня"), "лебединая песня")
        self.assertEqual(new_censor_filter("вкусный суп"), "вкусный суп")
        self.assertEqual(new_censor_filter("срубить дерево"), "срубить дерево") # from 'сру'
        self.assertEqual(new_censor_filter("трахтенберг"), "трахтенберг") # from 'трах'

    def test_edge_cases(self):
        self.assertEqual(new_censor_filter(""), "")
        self.assertEqual(new_censor_filter("!@#$%^&*()"), "!@#$%^&*()")
        self.assertEqual(new_censor_filter("просто текст без мата"), "просто текст без мата")
        self.assertEqual(new_censor_filter("слово"), "слово")
