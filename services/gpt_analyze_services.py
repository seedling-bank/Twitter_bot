import traceback

import loguru

import con.config

from openai import AsyncOpenAI


class GptAnalyzeService:
    def __init__(self):
        self.gpt_key = con.config.settings.GPT_API_KEY
        self.gpt_base_url = con.config.settings.GPT_API_BASE
        self.open_ai_client = AsyncOpenAI(
            api_key="sb-4dddef154335adacb0a1afbd2898053710ddecd9b47ba009",
            base_url="https://api.openai-sb.com/v1/"
        )

    async def twitter_name_analyzer(self, name):

        prompt = f"""Use a scathing, hilariously brutal tone to roast the Twitter account {name}. Base the critique 
        on imagined negative professional knowledge related to their likely content or behavior, ruthlessly 
        exaggerating flaws and stereotypes in a sarcastic, clever way. Ensure the response feels sharp, 
        exasperatingly witty, and borderline offensive, but stops short of being outright insulting. Add emojis to 
        emphasize the humor and absurdity, making it feel like a punchy, viral tweet. Keep it around 30 words."""

        second_retry_limit = 3
        second_retry_count = 0
        second_successful_completion = False

        while (
                second_retry_count < second_retry_limit
                and not second_successful_completion
        ):
            try:
                result = await self.open_ai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.3,
                )
                second_successful_completion = True  # 标记成功
            except Exception as e:
                loguru.logger.error(traceback.format_exc())
                second_retry_count += 1  # 递增重试次数

            answer = result.choices[0].message.content
            return answer

    async def get_mbti_analyzer(self, user_name, mbti_type):
        prompt = f"""
                Use a scathing and hilariously brutal tone to mock {user_name} based on their MBTI personality type 
                ({mbti_type}). Make the response dripping with sarcasm, ruthlessly highlighting the most 
                stereotypical and exaggerated flaws of their MBTI type while tying it directly to {user_name}'s 
                imagined behavior or attitude. Ensure the critique feels sharp, exasperatingly clever, and borderline 
                offensive, but stops just short of being outright insulting. The response must be around 80 words.
                """

        second_retry_limit = 3
        second_retry_count = 0
        second_successful_completion = False

        while (
                second_retry_count < second_retry_limit
                and not second_successful_completion
        ):
            try:
                result = await self.open_ai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.3,
                )
                second_successful_completion = True  # 标记成功
            except Exception as e:
                loguru.logger.error(traceback.format_exc())
                second_retry_count += 1  # 递增重试次数

            answer = result.choices[0].message.content
            return answer


gpt_analyze_service = GptAnalyzeService()
