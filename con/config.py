from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GPT_API_BASE: str = "https://api.openai-sb.com/v1/"
    GPT_API_KEY: str = "sb-4dddef154335adacb0a1afbd2898053710ddecd9b47ba009"

    APIDANCE_API_KEY: str = "veyizsgc0f5x4mbl5k4xmajxvkhjex"

    TWITTER_AUTH_TOKEN: str = "efb2cd709ed756e8ef34ba30ce7981af2addf6ca"
    TWITTER_ID: str = '4654805796'
    TWITTER_NAME: str = '@lyricpaxsrks'

    MAX_RETRIES: int = 5
    DELAY: int = 5

    # test
    # TWITTER_AUTH_TOKEN: str = "a702759db125fe810d9a8db8959b538abdcf094a"
    # TWITTER_ID: str = '1661204064376348672'
    # TWITTER_NAME: str = '@mr_gongmm'


settings = Settings()
