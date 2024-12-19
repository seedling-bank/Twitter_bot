from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GPT_API_BASE: str = "https://api.openai-sb.com/v1/"
    GPT_API_KEY: str = "sb-4dddef154335adacb0a1afbd2898053710ddecd9b47ba009"

    APIDANCE_API_KEY: str = "veyizsgc0f5x4mbl5k4xmajxvkhjex"

    # test
    # TWITTER_AUTH_TOKEN: str = "efb2cd709ed756e8ef34ba30ce7981af2addf6ca"
    # TWITTER_ID: str = '4654805796'
    # TWITTER_NAME: str = '@lyricpaxsrks'

    TWITTER_AUTH_TOKEN: str = "7628935482e0e6dc6e3db8e0fc9cd33829458d99"
    TWITTER_ID: str = '1913659728'
    TWITTER_NAME: str = '@MBTAI_'

    MAX_RETRIES: int = 5
    DELAY: int = 5

    # test
    # TWITTER_AUTH_TOKEN: str = "a702759db125fe810d9a8db8959b538abdcf094a"
    # TWITTER_ID: str = '1661204064376348672'
    # TWITTER_NAME: str = '@mr_gongmm'

    # 测试环境
    # DATABASE_URI: str = "mysql+aiomysql://root:mm123123@127.0.0.1:3306/mbti"
    # 正式环境
    DATABASE_URI: str = "mysql+aiomysql://cb:cryptoBricks123@cb-rds.cw5tnk9dgstt.us-west-2.rds.amazonaws.com:3306/mbti"

    # 测试环境Redis
    # REDIS_URL: str = "redis://10.244.4.140:6379/14"
    # 生产环境redis
    REDIS_URL: str = "redis://10.244.4.58:6379/14"
    # 本地环境Redis
    # REDIS_URL: str = "redis://127.0.0.1:6379/14"


settings = Settings()
