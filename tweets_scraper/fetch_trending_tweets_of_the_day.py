'''
to fetch trending tweets of the day
python fetch_trending_tweets_of_the_day.py
'''
# Imports
from time import sleep
import json
import datetime
import requests
import yaml

# Email ID scraping from twitter accounts
# # auth info

with open('config/trends_config.yaml', 'r') as file:
    trends_config = yaml.safe_load(file)

authorization = trends_config['authorization']
x_client_transaction_id = trends_config['x_client_transaction_id']
x_client_uuid = trends_config['x_client_uuid']
x_csrf_token =  trends_config['x_csrf_token']

def explore_trends(file_name: str = 'data/trending_tweets.txt'):
        

        url = "https://twitter.com/i/api/2/guide.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&include_ext_is_blue_verified=1&include_ext_verified_type=1&include_ext_profile_image_shape=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_ext_limited_action_results=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_ext_views=true&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&tab_category=objective_trends&count=20&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2CbirdwatchPivot%2CsuperFollowMetadata%2CunmentionInfo%2CeditControl"

        payload = {}
        headers = {
        'authority': 'twitter.com',
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.9',
        'authorization': authorization,
        'cookie': 'g_state={"i_p":1695038335856,"i_l":1}; lang=en; guest_id=v1%3A169503180163832738; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCC23xKeKAToMY3NyZl9p%250AZCIlODMwNTVhZmM3MTY4ODA0NGYwY2I4Mjg2MzEwZDNhOWQ6B2lkIiUxZGY1%250AY2M0ODZiNDk2MGNhNDYzNjIwZGM3ZjM2NmE0Mw%253D%253D--25f7619a17dc33a454797e2088ed2b77d3f29b55; guest_id_marketing=v1%3A169503180163832738; guest_id_ads=v1%3A169503180163832738; kdt=jBQSxlWxVUctZcQZJTSABeqMXnVnXQIbvD6rzlkx; auth_token=7dfba12762e63f0abcfdbbdb4786983a3b2e0590; ct0=11c09cdbb6f0eb342ce96fbfa7744a740a8cc5022ec319e342a24c0aeabd91c1e0a3130fddf8a8abd1df3a95737d28e6a642e1b32c36fc71fc1080fdb78d5d9ec61fa2fcf7071138e7b7415f598ac94f; twid=u%3D759797697679196160; personalization_id="v1_YnYCXWgG/OkRwFMdvCCGCw=="; guest_id=v1%3A169503345039396724; guest_id_ads=v1%3A169503345039396724; guest_id_marketing=v1%3A169503345039396724; personalization_id="v1_ZhDH2ziMkJLwWp1NqpROoQ=="',
        'referer': 'https://twitter.com/explore/tabs/trending',
        # 'sec-ch-ua': '"Brave";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'x-client-transaction-id': x_client_transaction_id,
        'x-client-uuid': x_client_uuid,
        'x-csrf-token': x_csrf_token,
        'x-twitter-active-user': 'yes',
        'x-twitter-auth-type': 'OAuth2Session',
        'x-twitter-client-language': 'en',
        'x-twitter-utcoffset': '+0530'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        twitter_json_response = response.text

        # print(f"{twitter_json_response=}")
        parsed_json = json.loads(twitter_json_response)

        # Pretty-print the JSON dictionary
        formatted_json = json.dumps(parsed_json, indent=4)
        print(formatted_json)

        # Open the text file in append mode
        with open(file_name, 'a') as file:
            # Parse the JSON string into a Python dictionary
            file.write(formatted_json + '\n')


# Get the current date in the format dd_mm
current_date = datetime.datetime.now().strftime('%d_%m')
file_name = f'data/trending_tweets_{current_date}.txt'



explore_trends(file_name)
