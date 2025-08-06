import re
import os

def get_profanity_regex_and_good_words():
    """
    Builds a regex to find potential profanity and returns it along with a set of good words.
    """
    char_map = {
        'а': '[aа@]', 'б': '[bб6]', 'в': '[vв]', 'г': '[gг]', 'д': '[dд]',
        'е': '[eеё]', 'ё': '[eеё]', 'ж': '[zhж]', 'з': '[zз3]', 'и': '[iи1]',
        'й': '[yй]', 'к': '[kк]', 'л': '[lл]', 'м': '[mм]', 'н': '[hн]',
        'о': '[oо0]', 'п': '[pп]', 'р': '[rр]', 'с': '[sсc]', 'т': '[tт]',
        'у': '[uуy]', 'ф': '[fф]', 'х': '[khхx]', 'ц': '[tsц]', 'ч': '[chч4]',
        'ш': '[shш]', 'щ': '[schщ]', 'ъ': '[\'"]?', 'ы': '[yы]', 'ь': '[\'"]?',
        'э': '[eэ]', 'ю': '[yuю]', 'я': '[yaя]'
    }

    try:
        with open(os.path.join(os.path.dirname(__file__), 'BadPartsOfWords.txt'), 'r', encoding='utf-8') as f:
            bad_words_text = re.sub(r'#.*?\n', '\n', f.read())
            bad_words = sorted([word for word in bad_words_text.split() if len(word) > 0], key=len, reverse=True)

        with open(os.path.join(os.path.dirname(__file__), 'GoodPartsOfWords.txt'), 'r', encoding='utf-8') as f:
            good_words_text = re.sub(r'#.*?\n', '\n', f.read())
            good_words = set(good_words_text.split())

    except FileNotFoundError:
        return None, None

    patterns = []
    separator = '[\\s\\-_\\.,!*]*'

    for root in bad_words:
        pattern_parts = []
        is_english = re.search(r'[a-zA-Z]', root)

        if is_english:
            patterns.append(re.escape(root) + r'\w*')
            continue

        for char in root.lower():
            pattern_parts.append(char_map.get(char, re.escape(char)) + '+')

        root_pattern = separator.join(pattern_parts)
        # Using a non-greedy suffix pattern
        suffix_pattern = r"(?:[a-zA-Zа-яА-ЯёЁ0-9]|[\\s\\-_\\.,!*])*?"
        patterns.append(f"{root_pattern}{suffix_pattern}")

    # Add special case for 3.14...
    patterns.append(r'3[\s\._-]*1[\s\._-]*4[\s\._-]*[zз3]+[\s\._-]*[dд]+[еeё]+[цc]+')

    final_regex = f"^(?:{'|'.join(patterns)})$"

    return re.compile(final_regex, re.IGNORECASE), good_words

PROFANITY_REGEX, GOOD_WORDS = get_profanity_regex_and_good_words()

def new_censor_filter(text: str) -> str:
    """
    Filters profanity by splitting text, checking against a profanity regex,
    and then verifying against a list of good words.
    """
    if not PROFANITY_REGEX or not text:
        return text

    parts = re.split(r'(\s+)', text)

    result_parts = []
    for part in parts:
        if not part or part.isspace():
            result_parts.append(part)
            continue

        if PROFANITY_REGEX.match(part):
            if part.lower() in GOOD_WORDS:
                result_parts.append(part)
            else:
                result_parts.append('*' * len(part))
        else:
            result_parts.append(part)

    return "".join(result_parts)
