from enum import Enum
from django.http import HttpResponse
from django.shortcuts import render
import re
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from censor_app import good_words, bad_words, bad_re_set
from transliterate import translit


class CensorFilter(APIView):

    def post(self, request) -> HttpResponse:
        censor_result = censor_filter(request.data.get("text"), request.data.get("method"))
        resp = {"text": censor_result[0],
                "bad_words": censor_result[1]}
        return Response(resp, status=status.HTTP_200_OK)


class CensorView(APIView):

    def get(self, request: any) -> HttpResponse:
        context = {
            'from_intext': 'Введите текст',
            'from_outtext': 'Здесь будет результат'
        }
        return render(request=request, template_name='censor_app/index.html', context=context)

    def post(self, request: any) -> HttpResponse:
        from_intext = request.POST.get('from-intext')
        if 'deep' in request.POST:
            from_outtext = censor_filter(from_intext, MethodType.deep)[0]

        elif 'fast' in request.POST:
            from_outtext = censor_filter(from_intext, MethodType.fast)[0]
        elif 'clear' in request.POST:
            from_intext = 'Введите текст'
            from_outtext = 'Здесь будет результат'
        else:
            from_outtext = censor_filter(from_intext, MethodType.deep)[0]

        context = {
            'from_intext': from_intext,
            'from_outtext': from_outtext
        }

        return render(request=request, template_name='censor_app/index.html', context=context)


class MethodType(Enum):
    deep = 'deep'
    fast = 'fast'


def censor_filter(message: str, method: MethodType) -> (str, list):
    # Выполняем посимвольный транслит для каждого слова текста сообщения
    message_list = re.findall(r"\w+|[^\w\s]", message)  # Разбиваем текст на отдельные слова и знаки препинания.
    bad_words_in_text = []
    result = ''
    for word_num in range(len(message_list)):
        word = message_list[word_num].lower()
        if 2 < len(word) < 26:  # фильтруем слова короче 25 и длиннее 2 букв
            word = remove_dup_chars(word)
            # Если в слове встречаются латинские символы или цифры
            if re.search(r'[a-zA-Z0-9]', word):
                good, bad = translit_good_bad_count(word)
            # Если в слове не встречаются латинские символы или цифры аналогично
            else:
                good, bad = good_bad_count(word)
            # Если плохих частей больше чем хороших
            if bad > good:
                bad_words_in_text.append(word)
                message_list[word_num] = "*" * len(word)
        elif word in ('еб', 'еп', 'eb', 'eб', 'eп'):  # Считаем все остальные слова короче 3 букв нормальными
            bad_words_in_text.append(word)  # Собираем неприличные слова для статистики
            message_list[word_num] = "**"
        elif len(word) > 25:  # Считаем все сова длиннее  25 символов неприличными
            bad_words_in_text.append(word)
            message_list[word_num] = "*" * len(word)
        if message_list[word_num] in [",", ".", ":", "!", "?", "...", ";", "'", "-"]:
            result += '' + message_list[word_num]
        else:
            result += (' ' if result != '' else '') + message_list[word_num]
        # Ищем в тексте совпадения с регулярными выражениями если выбран метод "deep"
    if method == MethodType.deep:
        result, bad_words_in_text = regular_sub(result, bad_words_in_text)
    return result, bad_words_in_text


def remove_dup_chars(word: str) -> str:
    result = ''
    current = ' '
    for n in range(len(word)):
        if current != word[n]:
            result += word[n]
            current = word[n]
    return result


def translit_good_bad_count(word: str) -> (int, int):
    good = 0  # счетчик хороших частей слов
    bad = 0  # счетчик плохих частей слов
    translit1 = translit(word, "ru1")
    translit2 = translit(word, "ru2")
    # Ищем в слове части неприличных слов
    for bad_word in bad_words:
        bad += max(translit1.count(bad_word), translit2.count(bad_word))
    # Если попались части плохих слов
    if bad > 0:
        # Ищем в слове части приличных слов
        for good_word in good_words:
            good += max(translit1.count(good_word), translit2.count(good_word))
    return good, bad


def good_bad_count(word: str) -> (int, int):
    good = 0  # счетчик хороших частей слов
    bad = 0  # счетчик плохих частей слов
    for bad_word in bad_words:
        bad += word.count(bad_word)
    if bad > 0:
        for good_word in good_words:
            good += word.count(good_word)
    return good, bad


def regular_sub(result: str, bad_words_in_text: list) -> (str, list):
    for bad_re in bad_re_set:
        if re.search(bad_re, result.lower()):
            mats = re.findall(bad_re, result.lower())
            bad_words_in_text.extend(mats)
            for mat in mats:
                result = re.sub(bad_re.pattern, "*" * len(mat), result, flags=re.IGNORECASE)
    return result, bad_words_in_text

# print(remove_dup_chars('козел') == 'козел')
