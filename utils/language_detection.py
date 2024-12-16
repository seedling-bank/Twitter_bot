import asyncio
import traceback

import loguru
from lingua import Language, LanguageDetectorBuilder

language = [
    Language.ENGLISH,  # 英语
    Language.CHINESE,  # 中文
    Language.JAPANESE,  # 日语
    Language.KOREAN,  # 韩语
    Language.FRENCH,
    Language.AFRIKAANS,
    Language.ALBANIAN,
    Language.ARABIC,
    Language.ARMENIAN,
    Language.AZERBAIJANI,
    Language.INDONESIAN,  #
    Language.BASQUE,
    Language.BELARUSIAN,
    Language.GERMAN,
    Language.SPANISH,
    Language.BENGALI,
    Language.BOKMAL,
    Language.BOSNIAN,
    Language.BULGARIAN,
    Language.CATALAN,
    Language.CROATIAN,
    Language.CZECH,
    Language.DANISH,
    Language.DUTCH,
    Language.ESPERANTO,
    Language.ESTONIAN,
    Language.FINNISH,
    Language.GANDA,
    Language.GEORGIAN,
    Language.GREEK,
    Language.GUJARATI,
    Language.HEBREW,
    Language.HINDI,
    Language.HUNGARIAN,
    Language.ICELANDIC,
    Language.INDONESIAN,
    Language.IRISH,
    Language.ITALIAN,
    Language.KAZAKH,
    Language.LATIN,
    Language.LATVIAN,
    Language.LITHUANIAN,
    Language.MACEDONIAN,
    Language.MALAY,
    Language.MAORI,
    Language.MARATHI,
    Language.MONGOLIAN,
    Language.NYNORSK,
    Language.PERSIAN,
    Language.POLISH,
    Language.PORTUGUESE,
    Language.PUNJABI,
    Language.ROMANIAN,
    Language.RUSSIAN,
    Language.SERBIAN,
    Language.SHONA,
    Language.SLOVAK,
    Language.SLOVENE,
    Language.SOMALI,
    Language.SOTHO,
    Language.SWAHILI,
    Language.SWEDISH,
    Language.TAGALOG,
    Language.TAMIL,
    Language.TELUGU,
    Language.THAI,
    Language.TSONGA,
    Language.TSWANA,
    Language.TURKISH,
    Language.UKRAINIAN,
    Language.URDU,
    Language.VIETNAMESE,
    Language.WELSH,
    Language.XHOSA,
    Language.YORUBA,
    Language.ZULU,
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

