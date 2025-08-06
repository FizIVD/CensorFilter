from django.http import HttpResponse
from django.shortcuts import render
import re
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from censor_app import numbers_set
from .new_censor import new_censor_filter


class CensorFilter(APIView):

    def post(self, request) -> HttpResponse:
        # The new filter is efficient, so we can use it for all requests.
        # The distinction between 'deep' and 'fast' is no longer necessary.
        filtered_text = new_censor_filter(request.data.get("text"))
        # The new filter doesn't return a list of bad words, so we return an empty list.
        resp = {"text": filtered_text,
                "bad_words": []}
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

        if 'clear' in request.POST:
            from_intext = 'Введите текст'
            from_outtext = 'Здесь будет результат'
        else:
            # All filtering modes now use the new, more efficient filter.
            from_outtext = new_censor_filter(from_intext)
            # The phone substitution can be run after the main filter.
            if 'deep' in request.POST:
                 from_outtext = regular_phone_sub(from_outtext)

        context = {
            'from_outtext': from_outtext
        }

        return render(request=request, template_name='censor_app/index.html', context=context)


def regular_phone_sub(result: str) -> str:
    # This function seems to be for censoring phone numbers and is separate from profanity.
    # I will leave it as is.
    numbers = []
    for number in numbers_set:
        if number in result.lower():
            n = result.count(number)
            numbers.extend([number] * n)
    if len(numbers) > 9:
        for number in numbers:
            result = re.sub(number, "*" * len(number), result, flags=re.IGNORECASE)
    result = re.sub('\+?\W?[\d\W*o?O?о?О?]{9}\d\d?', '*' * 11, result)
    return result
