import asyncio
import traceback

import loguru
import google.generativeai as genai

import con.config


class MBTIService:
    def __init__(self):
        pass

    async def get_user_mbti_analyze(self, data, user_name: str):
        try:

            for attempt in range(1, con.config.settings.MAX_RETRIES + 1):
                try:
                    result = await self.mbti_genai_analysis(data=data, name=user_name)

                    if result is not None:
                        return result
                except Exception as e:
                    loguru.logger.error(e)
                    loguru.logger.error(traceback.format_exc())
                await asyncio.sleep(con.config.settings.DELAY)
            return None
        except Exception as e:
            loguru.logger.error(e)
            loguru.logger.error(traceback.format_exc())
            return False

    async def mbti_genai_analysis(self, data, name):
        try:
            genai.configure(api_key="AIzaSyAk7VmYzRN1IG9GiRf3luB1jHrgzkcOUac")
            model = genai.GenerativeModel("gemini-1.5-flash")
            test = f"""
                        text: '# User Tweets

                        {data}

                        # Steps to Perform

                        Extract recent tweets from the user and combine them with the bio content to infer the user's potential preferences/profession/habits.

                        Infer the user's MBTI. The judgment criteria are as follows:

                        I/E:

                        I: Introverted individuals prefer solitary activities and get exhausted
                        by social interaction. They tend to be quite sensitive to external stimulation
                        (e.g. sound, sight or smell) in general. / E: Extraverted individuals
                        prefer group activities and get energized by social interaction. They
                        tend to be more enthusiastic and more easily excited than Introverts.

                        S/N:

                        S: Observant individuals are highly practical, pragmatic and down-to-earth.
                        They tend to have strong habits and focus on what is happening or has
                        already happened. / N: Intuitive individuals are very imaginative, open-minded
                        and curious. They prefer novelty over stability and focus on hidden meanings
                        and future possibilities.

                        T/F:

                        T: Thinking individuals focus on objectivity and rationality, prioritizing
                        logic over emotions. They tend to hide their feelings and see efficiency
                        as more important than cooperation. / F: Feeling individuals are sensitive
                        and emotionally expressive. They are more empathic and less competitive
                        than Thinking types, and focus on social harmony and cooperation.

                        J/P:

                        J: Judging individuals are decisive, thorough and highly organized. They
                        value clarity, predictability and closure, preferring structure and planning
                        to spontaneity. / P: Prospecting individuals are very good at improvising
                        and spotting opportunities. They tend to be flexible, relaxed nonconformists
                        who prefer keeping their options open.

                        Remember the analysis results, and use them in the analysis report to be output. Make sure the results match Twitter's style, add some necessary emojis. The length limit is around 30 words.
                        """

            response = model.generate_content(test)
            return response.text
        except Exception as e:
            loguru.logger.error(e)
            loguru.logger.error(traceback.format_exc())


mbti_service = MBTIService()
