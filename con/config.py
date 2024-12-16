from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GPT_API_BASE: str = "https://api.openai-sb.com/v1/"
    GPT_API_KEY: str = "sb-4dddef154335adacb0a1afbd2898053710ddecd9b47ba009"

    APIDANCE_API_KEY: str = "veyizsgc0f5x4mbl5k4xmajxvkhjex"

    TWITTER_AUTH_TOKEN: str = "efb2cd709ed756e8ef34ba30ce7981af2addf6ca"

    MAX_RETRIES: int = 5
    DELAY: int = 5

    TWITTER_ID: str = '4654805796'


settings = Settings()
