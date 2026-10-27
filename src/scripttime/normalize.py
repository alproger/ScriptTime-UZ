"""Conservative orthographic normalization for retrieval experiments.

This is lossy; it is NOT a normative Uzbek transliteration standard.
Always preserve original text for display/citation.
"""
import re
import unicodedata

CYR = {
    "а":"a", "б":"b", "в":"v", "г":"g", "д":"d", "е":"e", "ё":"yo", "ж":"j",
    "з":"z", "и":"i", "й":"y", "к":"k", "л":"l", "м":"m", "н":"n", "о":"o",
    "п":"p", "р":"r", "с":"s", "т":"t", "у":"u", "ф":"f", "х":"x", "ц":"ts",
    "ч":"ch", "ш":"sh", "ъ":"'", "ь":"", "э":"e", "ю":"yu", "я":"ya",
    "ў":"o'", "қ":"q", "ғ":"g'", "ҳ":"h",
}
APOS = "’‘ʼʻ`´ʹ＇ꞌʽ′"


def normalize(text: str) -> str:
    """Map selected Cyrillic/new-Latin/legacy-Latin variants to a common form."""
    text = unicodedata.normalize("NFKC", text).casefold()
    text = "".join(CYR.get(ch, ch) for ch in text)
    for mark in APOS:
        text = text.replace(mark, "'")
    text = text.replace("ö", "o'").replace("ğ", "g'")
    text = text.replace("ş", "sh").replace("ç", "ch")
    return " ".join(re.findall(r"[a-z0-9']+", text))


def tokens(text: str, normalize_first: bool = False) -> list[str]:
    if normalize_first:
        text = normalize(text)
    else:
        text = unicodedata.normalize("NFKC", text).casefold()
    return re.findall(r"[a-z0-9öğşçа-яёқғўҳʼ'‘’]+", text)
