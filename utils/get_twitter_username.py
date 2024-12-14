async def get_twitter_username(data):
    try:
        if data:
            tweets = data.get('tweets', None)
            if tweets:
                for tweet in tweets:
                    user_info = tweet.get('user', None)
                    if user_info:
                        user_id = user_info.get('id_str', None)
                        user_name = user_info.get('name', None)
                        user_username = user_info.get('screen_name', None)
                        information = {
                            'user_id': user_id,
                            'user_name': user_name,
                            'user_username': user_username
                        }
                        result = verify_user_duplication(user_id=user_id)
                        if result:
                            return information
    except Exception as e:
        loguru.logger.error(e)
        loguru.logger.error(traceback.format_exc())