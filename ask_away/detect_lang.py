import re
from typing import List, Tuple


def detect_lang_code(text: str) -> List[Tuple[str, str]]:
    """Detects all languages and code used in the given text.

    Args:
        text (str): The text.
    """
    # https://stackoverflow.com/questions/8303488/regex-to-match-any-character-including-new-lines
    return re.findall(r"```(.*?)\n+((?s:.)+?)\n*```", text)
