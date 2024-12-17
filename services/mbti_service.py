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
            text: '# 用户推文

            {data}

            # 执行步骤

            从用户推文中获取近期推文，并且结合简介内容推断用户可能的喜好/职业/习惯

            推断用户的MBTI，判断标准如下：

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

            请记住分析的结果，要输出的分析报告中要使用这个结果，使结果满足twitter的风格，添加一些必要的emoji。长度限制为30词左右。
            """
            response = model.generate_content(test)
            return response.text
        except Exception as e:
            loguru.logger.error(e)
            loguru.logger.error(traceback.format_exc())


mbti_service = MBTIService()
