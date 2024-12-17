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
                                                            items = content.get('items', None)
                                                            if itemContent:
                                                                itemContent = itemContent
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
                                                                itemContent = items
                                                                for item in itemContent:
                                                                    item_a = item.get('item', None)
                                                                    itemContent = item_a.get('itemContent', None)
                                                                    tweet_results = itemContent.get('tweet_results',
                                                                                                    None)
                                                                    if tweet_results:
                                                                        result = tweet_results.get('result', None)
                                                                        if result:
                                                                            user_twitter_id = result.get('rest_id',
                                                                                                         None)
                                                                            if user_twitter_id:
                                                                                user_twitter_list.append(
                                                                                    user_twitter_id)
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

            return user_twitter_list
        except Exception as e:
            loguru.logger.error(e)
            loguru.logger.error(traceback.format_exc())

    def user_tweets_and_replies_analysis(self, user_data):
        user_twitter_list = list()
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
                                for instruction in instructions:
                                    if instruction.get('type') == "TimelineAddEntries":
                                        entries = instruction.get('entries', None)
                                        for entry_index, entry in enumerate(entries):
                                            if entry_index >= len(entries) - 2:
                                                continue
                                            content = entry.get('content', None)
                                            if content:
                                                items = content.get('items', None)
                                                if items:
                                                    for item_row in items:
                                                        item = item_row.get('item', None)
                                                        if item:
                                                            itemContent = item.get('itemContent', None)
                                                            if itemContent:
                                                                tweet_results = itemContent.get('tweet_results', None)
                                                                if tweet_results:
                                                                    result = tweet_results.get('result', None)
                                                                    if result:
                                                                        legacy = result.get('legacy', None)
                                                                        if legacy.get(
                                                                                'in_reply_to_screen_name') != 'lyricpaxsrks':
                                                                            information = {
                                                                                'twitter_id': legacy.get('id_str'),
                                                                                'twitter_content': legacy.get(
                                                                                    'full_text'),
                                                                            }
                                                                            user_twitter_list.append(information)
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
                if tweets:
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

    def get_search_resul_analysis(self, datas):
        if datas:
            response_list_required = list()
            for index, data in enumerate(datas):
                information = {
                    "tweet_id": data['tweet_id'],
                    "tweet_content": data['text'],
                    'id_str': data['user']['id_str'],
                    "tweet_name": data['user']['screen_name'],
                }
                response_list_required.append(information)
            return response_list_required

    def user_twitter_processing(self, user_data):
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
                                                    text_list = ""
                                                    for index_entrie, entrie in enumerate(entries):
                                                        if index_entrie >= 5:
                                                            break
                                                        content = entrie.get('content', None)
                                                        if content:
                                                            itemContent = content.get('itemContent', None)
                                                            if itemContent:
                                                                tweet_results = itemContent.get('tweet_results', None)
                                                                if tweet_results:
                                                                    result = tweet_results.get('result', None)
                                                                    if result:
                                                                        tweet = result.get('tweet', None)
                                                                        if tweet:
                                                                            legacy = tweet.get('legacy', None)
                                                                        else:
                                                                            legacy = result.get('legacy', None)
                                                                            if legacy:
                                                                                full_text = legacy.get('full_text',
                                                                                                       None)
                                                                                text_list += (str(
                                                                                    index_entrie + 1)
                                                                                              + '.' + full_text + '\n')
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
                                                    return text_list
            else:
                return None
        except Exception as e:
            loguru.logger.error(e)
            loguru.logger.error(traceback.format_exc())


twitter_service = TwitterService()
