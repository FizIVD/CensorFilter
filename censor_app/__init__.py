import os
import re
from transliterate.discover import autodiscover
from transliterate.base import TranslitLanguagePack, registry

autodiscover()


def read_file(name: str):
    open_file = open(os.path.dirname(__file__) + f"/{name}", encoding="utf-8")
    custom_set = set(re.sub("#.+\n", " ", open_file.read()).split(" "))
    open_file.close()
    custom_set.discard("")
    return custom_set


def re_custom_set(current_set: set):
    re_list = []
    for word in current_set:
        word_list = list(word)
        for let_num in range(len(word_list)):
            word_list[let_num] = word_list[let_num] + "\\W*_*"

        re_list.append(re.compile(f"\\b{''.join(word_list)}\\b"))
    re_set = set(re_list)
    return re_set


bad_words = read_file("BadPartsOfWords.txt")
good_words = read_file("GoodPartsOfWords.txt")
bad_re_set = re_custom_set(bad_words)

class RussianLanguagePack1(TranslitLanguagePack):
    language_code = "ru1"
    language_name = "Russian1"
    mapping = (
        u"a@b6vgdez3i!j*klmno0prs5$tufhcy'948",
        u"ааббвгдеззиижжклмноопрсcстуфхцыьячв",
    )
    pre_processor_mapping = {
        u"zh": u"ж",
        u"ts": u"ц",
        u"tc": u"ц",
        u"ch": u"ч",
        u"sh": u"ш",
        u"sch": u"щ",
        u"ju": u"ю",
        u"yu": u"ю",
        u"iu": u"ю",
        u"ja": u"я",
        u"ia": u"я",
        u"ya": u"я",
        u"q": u"к",
        u"wh": u"у",
        u"w": u"в",
        u"oo": u"у",
        u"ee": u"и",
        u"ck": u"к",
        u"yo": u"ё",
        u"yi": u"ий",
        u"ui": u"уй",
        u"x": u"кс",
    }


registry.register(RussianLanguagePack1)


class RussianLanguagePack2(TranslitLanguagePack):
    language_code = "ru2"
    language_name = "Russian2"
    mapping = (
        u"a@b6vrdez3i!uj*gklmho0npcs5$tyfx'948",
        u"ааббвгдез3йиийжжклмноопрсcсстуфхьячв",
    )
    pre_processor_mapping = {
        u"zh": u"ж",
        u"ts": u"ц",
        u"tc": u"ц",
        u"ch": u"ч",
        u"sh": u"ш",
        u"sch": u"щ",
        u"ju": u"ю",
        u"yu": u"ю",
        u"iu": u"ю",
        u"ja": u"я",
        u"ia": u"я",
        u"ya": u"я",
        u"q": u"а",
        u"wh": u"у",
        u"w": u"ш",
        u"oo": u"у",
        u"ee": u"и",
        u"ck": u"к",
        u"yo": u"ё",
    }


registry.register(RussianLanguagePack2)
