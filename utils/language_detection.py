import asyncio
import traceback

import loguru
from lingua import Language, LanguageDetectorBuilder

language = [
    Language.ENGLISH,  # 英语
    Language.CHINESE,  # 中文
    Language.JAPANESE,  # 日语
    # Language.KOREAN,  # 韩语
    # Language.FRENCH,  # 法语
    # Language.AFRIKAANS,
    # Language.ALBANIAN,
    # Language.ARABIC,    # 阿拉伯语
    # Language.ARMENIAN,
    # Language.AZERBAIJANI,
    # Language.INDONESIAN,
    # Language.BASQUE,
    # Language.BELARUSIAN,
    # Language.GERMAN,    # 德语
    # Language.SPANISH,   # 西班牙语
    # Language.BENGALI,
    # Language.BOKMAL,
    # Language.BOSNIAN,
    # Language.BULGARIAN,
    # Language.CATALAN,
    # Language.CROATIAN,
    # Language.CZECH,
    # Language.DANISH,
    # Language.DUTCH,
    # Language.ESPERANTO,
    # Language.ESTONIAN,
    # Language.FINNISH,
    # Language.GANDA,
    # Language.GEORGIAN,
    # Language.GREEK,
    # Language.GUJARATI,
    # Language.HEBREW,
    # Language.HINDI,
    # Language.HUNGARIAN,
    # Language.ICELANDIC,
    # Language.INDONESIAN,
    # Language.IRISH,
    # Language.ITALIAN,
    # Language.KAZAKH,
    # Language.LATIN,
    # Language.LATVIAN,
    # Language.LITHUANIAN,
    # Language.MACEDONIAN,
    # Language.MALAY,
    # Language.MAORI,
    # Language.MARATHI,
    # Language.MONGOLIAN,
    # Language.NYNORSK,
    # Language.PERSIAN,
    # Language.POLISH,
    # Language.PORTUGUESE, # 葡萄牙语
    # Language.PUNJABI,
    # Language.ROMANIAN,
    # Language.RUSSIAN, # 俄语
    # Language.SERBIAN,
    # Language.SHONA,
    # Language.SLOVAK,
    # Language.SLOVENE,
    # Language.SOMALI,
    # Language.SOTHO,
    # Language.SWAHILI,     # 斯瓦希里语
    # Language.SWEDISH,
    # Language.TAGALOG,
    # Language.TAMIL,
    # Language.TELUGU,
    # Language.THAI,  # 泰语
    # Language.TSONGA,
    # Language.TSWANA,
    # Language.TURKISH,   #土耳其语
    # Language.UKRAINIAN,
    # Language.URDU,
    # Language.VIETNAMESE,    # 越南语
    # Language.WELSH,
    # Language.XHOSA,
    # Language.YORUBA,
    # Language.ZULU,
]
detector = LanguageDetectorBuilder.from_languages(*language).build()


async def language_detection(tweet):
    """对输入的语言进行检测，"""
    try:
        result = detector.detect_language_of(tweet)
        return result
    except Exception as e:
        loguru.logger.error(e)
        loguru.logger.error(traceback.format_exc())
