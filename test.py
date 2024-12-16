import asyncio
import traceback

import loguru

data = {"data": {"create_tweet": {"tweet_results": {"result": {"core": {"user_results":
                                                                            {"result": {"__typename": "User",
                                                                                        "affiliates_highlighted_label": {},
                                                                                        "has_graduated_access": True
                                                                                , "id": "VXNlcjo0NjU0ODA1Nzk2",
                                                                                        "is_blue_verified": False
                                                                                , "legacy": {"can_dm": True,
                                                                                             "can_media_tag": True,
                                                                                             "created_at": "Sat Dec 26 11:14:17 +0000 2015"
                                                                                    , "default_profile": True,
                                                                                             "default_profile_image": False
                                                                                    ,
                                                                                             "description": "Risks must be taken, because the greatest hazard in life is to risk nothing."
                                                                                    , "entities": {
                                                                                        "description": {"urls": []}},
                                                                                             "fast_followers_count": 0,
                                                                                             "favourites_count": 17
                                                                                    , "followers_count": 971,
                                                                                             "friends_count": 1749,
                                                                                             "has_custom_timelines": False
                                                                                    , "is_translator": False,
                                                                                             "listed_count": 0,
                                                                                             "location": "",
                                                                                             "media_count": 0
                                                                                    , "name": "Testing",
                                                                                             "needs_phone_verification": False,
                                                                                             "normal_followers_count": 971
                                                                                    , "pinned_tweet_ids_str": [],
                                                                                             "possibly_sensitive": False
                                                                                    ,
                                                                                             "profile_image_url_https": "https://pbs.twimg.com/profile_images/1849020276174102528/OtMhYcDU_normal.jpg"
                                                                                    , "profile_interstitial_type": "",
                                                                                             "screen_name": "lyricpaxsrks",
                                                                                             "statuses_count": 55
                                                                                    , "translator_type": "none",
                                                                                             "verified": False,
                                                                                             "want_retweets": False
                                                                                    , "withheld_in_countries": []},
                                                                                        "profile_image_shape": "Circle",
                                                                                        "rest_id": "4654805796"}}}
    , "edit_control":
                                                                   {"edit_tweet_ids": ["1868559812046557237"]
                                                                       , "editable_until_msecs": "1734337950000"
                                                                       , "edits_remaining": "5",
                                                                    "is_edit_eligible": False}
    , "is_translatable": False
    , "legacy": {"bookmark_count": 0, "bookmarked": False
        , "conversation_id_str": "1867412735946109218"
        , "created_at": "Mon Dec 16 07:32:30 +0000 2024"
        , "display_text_range": [11, 29]
        , "entities": {"hashtags": [], "symbols": []
            , "urls": [], "user_mentions":
                           [{"id_str": "1661204064376348672"
                                , "indices": [0, 10]
                                , "name": "mr.gong"
                                , "screen_name": "mr_gongmm"}]}
        , "favorite_count": 0, "favorited": False
        , "full_text": "@mr_gongmm this is am example"
        , "id_str": "1868559812046557237"
        , "in_reply_to_screen_name": "mr_gongmm"
        , "in_reply_to_status_id_str": "1867412735946109218"
        , "in_reply_to_user_id_str": "1661204064376348672"
        , "is_quote_status": False, "lang": "en"
        , "quote_count": 0, "reply_count": 0
        , "retweet_count": 0, "retweeted": False
        , "user_id_str": "4654805796"}
    , "rest_id": "1868559812046557237"
    , "source": "\u003ca href=\"https://twitter.com\" rel=\"nofollow\"\u003eTweetDeck Web App\u003c/a\u003e"
    , "unmention_data": {}, "unmention_info": {}
    , "views": {"state": "Enabled"}}}}}}





async def main():
    await get_reply_id(data)

if __name__ == '__main__':
    asyncio.run(main())
