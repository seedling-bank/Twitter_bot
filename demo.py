data = {"pinned_tweet": None, "tweets":
    [{"tweet_id": "1867412735946109218", "user_id": "1661204064376348672", "media_type": ""
         , "text": "this is my first\n😀😀", "medias": None, "is_self_send": True, "is_retweet": False, "is_quote": False
         , "is_reply": False, "is_like": False, "related_tweet_id": "", "related_user_id": "", "favorite_count": 0
         , "quote_count": 0, "reply_count": 1, "retweet_count": 0, "created_at": "Fri Dec 13 03:34:25 +0000 2024"
         , "user": {"id_str": "1661204064376348672", "name": "mr.gong", "screen_name": "mr_gongmm", "location": ""
            , "description": "", "followers_count": 3, "friends_count": 3
            , "created_at": "Wed May 24 02:54:58 +0000 2023", "favourites_count": 0, "verified": False
            , "statuses_count": 16, "media_count": 0
            ,
                    "profile_image_url_https": "https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png"}}
        ,
     {"tweet_id": "1867423121026035878", "user_id": "1709536223294017537", "media_type": "", "text": "@mr_gongmm 你好啊"
         , "medias": None, "is_self_send": False, "is_retweet": False, "is_quote": False, "is_reply": True,
      "is_like": False
         , "related_tweet_id": "1867412735946109218", "related_user_id": "1661204064376348672", "favorite_count": 0
         , "quote_count": 0, "reply_count": 2, "retweet_count": 0, "created_at": "Fri Dec 13 04:15:41 +0000 2024"
         , "user": {"id_str": "1709536223294017537", "name": "miaomiao gong", "screen_name": "gong_miaom21101"
         , "location": "", "description": "", "followers_count": 1, "friends_count": 1
         , "created_at": "Wed Oct 04 11:49:48 +0000 2023", "favourites_count": 7, "verified": False
         , "statuses_count": 17, "media_count": 0
         , "profile_image_url_https": "https://pbs.twimg.com/profile_images/1709536293192118272/MEafgBpK_normal.png"}}
        , {"tweet_id": "1867805592523608559", "user_id": "1661204064376348672", "media_type": ""
         , "text": "@gong_miaom21101 Hi, you are awesome.", "medias": None, "is_self_send": False, "is_retweet": False
         , "is_quote": False, "is_reply": True, "is_like": False, "related_tweet_id": "1867423121026035878"
         , "related_user_id": "1709536223294017537", "favorite_count": 0, "quote_count": 0, "reply_count": 1
         , "retweet_count": 0, "created_at": "Sat Dec 14 05:35:30 +0000 2024"
         , "user": {"id_str": "1661204064376348672", "name": "mr.gong", "screen_name": "mr_gongmm", "location": ""
            , "description": "", "followers_count": 3, "friends_count": 3
            , "created_at": "Wed May 24 02:54:58 +0000 2023", "favourites_count": 0, "verified": False
            , "statuses_count": 16, "media_count": 0
            ,
                    "profile_image_url_https": "https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png"}}
        , {"tweet_id": "1867465250964189230", "user_id": "1661204064376348672", "media_type": "", "text": "hello"
         , "medias": None, "is_self_send": True, "is_retweet": False, "is_quote": False, "is_reply": False,
           "is_like": False
         , "related_tweet_id": "", "related_user_id": "", "favorite_count": 0, "quote_count": 0, "reply_count": 0
         , "retweet_count": 0, "created_at": "Fri Dec 13 07:03:06 +0000 2024"
         , "user": {"id_str": "1661204064376348672", "name": "mr.gong", "screen_name": "mr_gongmm", "location": ""
            , "description": "", "followers_count": 3, "friends_count": 3
            , "created_at": "Wed May 24 02:54:58 +0000 2023", "favourites_count": 0, "verified": False
            , "statuses_count": 16, "media_count": 0
            ,
                    "profile_image_url_https": "https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png"}}]
    , "next_cursor_str": ""}


def reply_analysis(data):
    if data:
        tweets = data.get('tweets', None)
        for tweet in tweets:
            if tweet.get('user_id') == "1661204064376348672":
                continue
            print(tweet)


if __name__ == '__main__':
    reply_analysis(data)
