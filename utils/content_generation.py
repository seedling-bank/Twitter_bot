import traceback

import loguru


async def twitter_content_generation(analyze_content, user_info):
    """
    生成需要发布的推文
    :param analyze_content:
    :param user_info:
    :return:
    """
    try:
        if analyze_content and user_info:
            twitter_content = analyze_content + "\n" + f"@{user_info['user_username']}"
            return twitter_content
    except Exception as e:
        loguru.logger.error(e)
        loguru.logger.error(traceback.format_exc())