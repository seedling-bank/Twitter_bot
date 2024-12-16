import json
import traceback

import loguru

import con.config
from utils.user_duplication import verify_user_duplication


class TwitterService:

    def __init__(self):
        pass

    def get_twitter_username(self, data):
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

    def user_data_processing(self, user_data):
        user_twitter_list = list()
        try:
            if user_data:
                data = user_data.get('data', None)
                if data:
                    user = data.get('user', None)
                    if user:
                        result = user.get('result', None)
                        if result:
                            timeline_v2 = result.get('timeline_v2', None)
                            if timeline_v2:
                                timeline = timeline_v2.get('timeline', None)
                                if timeline:
                                    instructions = timeline.get('instructions', None)
                                    if instructions:
                                        for index_instruction, instruction in enumerate(instructions):
                                            if instruction.get('type') == "TimelineAddEntries":
                                                entries = instruction.get('entries', None)
                                                if entries:
                                                    for index_entrie, entrie in enumerate(entries):
                                                        if index_entrie >= len(entries) - 2:
                                                            break
                                                        content = entrie.get('content', None)
                                                        if content:
                                                            itemContent = content.get('itemContent', None)
                                                            if itemContent:
                                                                tweet_results = itemContent.get('tweet_results', None)
                                                                if tweet_results:
                                                                    result = tweet_results.get('result', None)
                                                                    if result:
                                                                        user_twitter_id = result.get('rest_id', None)
                                                                        if user_twitter_id:
                                                                            user_twitter_list.append(user_twitter_id)
                                                                        else:
                                                                            pass
                                                                    else:
                                                                        return None
                                                                else:
                                                                    return None
                                                            else:
                                                                return None
                                                        else:
                                                            return None
                                else:
                                    return None
                            else:
                                return None
                        else:
                            return None
                    else:
                        return None
                else:
                    return None
            else:
                return None

            return user_twitter_list
        except Exception as e:
            loguru.logger.error(e)
            loguru.logger.error(traceback.format_exc())

    def remove_current_user(self, data):
        """
        获取待回复待列表
        :param data:
        :return:
        """
        twitter_ids = list()
        try:
            if data:
                print(data)
                tweets = data.get('tweets', None)
                for tweet in tweets:
                    if tweet.get('user_id') == con.config.settings.TWITTER_ID:
                        continue
                    else:
                        information = {
                            "tweet_id": tweet.get('tweet_id'),
                            "text": tweet.get('text'),
                            "screen_name": tweet.get('screen_name')
                        }
                        twitter_ids.append(information)
            else:
                return None
            print(f"twitter_ids--------{twitter_ids}")
            return twitter_ids
        except Exception as e:
            loguru.logger.error(e)
            loguru.logger.error(traceback.format_exc())

    def get_reply_id(self, user_data):
        try:
            if user_data:
                data = user_data.get('data', None)
                if data:
                    create_tweet = data.get('create_tweet', None)
                    if create_tweet:
                        tweet_results = create_tweet.get('tweet_results', None)
                        if tweet_results:
                            result = tweet_results.get('result', None)
                            if result:
                                twitter_id = result.get('rest_id')
                                return twitter_id
                            else:
                                return None
                        else:
                            return None
                    else:
                        return None
                else:
                    return None
            else:
                return None
        except Exception as e:
            loguru.logger.error(e)
            loguru.logger.error(traceback.format_exc())


twitter_service = TwitterService()
