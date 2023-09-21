'''
to run and fetch response for a specific search query on twitter

python search_query_tweets.py

auth token must be updated if session expires, and always add a sleep time of 1s, 

user-agent - can be skipped to avoid ip blocking
'''
import requests
import pickle
import json
import urllib.parse
import yaml
import datetime
import logging

import sys
import os

root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_directory)

# Email ID scraping from twitter accounts
# # auth info

with open('config/auth.yaml', 'r') as file:
    search_config = yaml.safe_load(file)

authorization = search_config['authorization']
x_client_transaction_id = search_config['x_client_transaction_id']
x_client_uuid = search_config['x_client_uuid']
x_csrf_token =  search_config['x_csrf_token']
cookie = search_config['cookie']

def generate_twitter_search_url(search_word):
    # URL-encode the search word
    encoded_search_word = urllib.parse.quote(search_word)

    # Define the URL template with placeholders for variables
    url_template = "https://twitter.com/i/api/graphql/3Ej-6N7xXONuEp5eJa1TdQ/SearchTimeline?variables=%7B%22rawQuery%22%3A%22{}%22%2C%22count%22%3A20%2C%22querySource%22%3A%22typed_query%22%2C%22product%22%3A%22Top%22%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"

    # Format the URL with the encoded search word
    url = url_template.format(encoded_search_word)

    return url




def search_tweets(search_query: str, twitter_search_url: str, referer: str):

    # url = "https://twitter.com/i/api/2/guide.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&include_ext_is_blue_verified=1&include_ext_verified_type=1&include_ext_profile_image_shape=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_ext_limited_action_results=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_ext_views=true&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&count=40&cursor=DefaultTopCursorValue&display_location=web_sidebar&include_page_configuration=false&entity_tokens=false&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2CbirdwatchPivot%2CsuperFollowMetadata%2CunmentionInfo%2CeditControl"
    url = twitter_search_url
    payload = {}
    headers = {
    'authority': 'twitter.com',
    'accept': '*/*',
    'accept-language': 'en-GB,en;q=0.9',
    'authorization': authorization,
    'cookie': cookie,
    'referer': referer,
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

    # print(response.text)
    twitter_json_response = response.text
    parsed_json = json.loads(twitter_json_response)

    # Pretty-print the JSON dictionary
    formatted_json = json.dumps(parsed_json, indent=4)
    # print(formatted_json)

   
    search_date = datetime.datetime.now().strftime('%d-%m-%Y')
    # New entry
    search_tweet_meta = {'search_date': search_date, 'search_query': search_query, 'search_results': parsed_json}
    
    # Read the existing JSON file
    try:
        with open('data/search_query_compilation.json', 'r') as file:
            data = json.load(file)
            
        print(f"{type(data)=}, {len(data)=}")
        # print(f"{data=}")
        # Find the index of an existing entry with the same date or -1 if not found
        new_data = data.copy()
        match_doc = -1
        
        for index, doc in enumerate(data):
            print(f"{index=}, {doc=}")
            if doc['search_query'] == search_tweet_meta["search_query"] and doc['search_date'] == search_tweet_meta["search_date"]:
                # Overwrite the existing entry with the same date
                new_data[index]['search_results'] = parsed_json
                # as a matching doc with same search query and on the same date already found and updated
                match_doc = 1
                break
        
        if match_doc == -1:
                # If no match is found, append the new entry
                new_data.append(search_tweet_meta)

        # Write back to the JSON file
        with open('data/search_query_compilation.json', 'w') as file:
            json.dump(new_data, file)

    except FileNotFoundError:
        logging.exception('created new search results compilation json')
        with open('data/search_query_compilation.json', 'w') as json_file:
            search_tweet_meta_list = [search_tweet_meta]
            json.dump(search_tweet_meta_list, json_file)

    return search_tweet_meta


def set_referer(search_query: str = ''):
    referer = 'https://twitter.com/search?q='
    search_words = search_query.split(' ')
    for s in search_words:
        referer += s + '%20'

    referer = referer.strip('%20')
    referer += '&src=typed_query'

    return referer

def set_file_name(search_query: str = 'search_tweet.txt'):
    search_words = search_query.split(' ')
    filename = 'data/search_tweet'
    for s in search_words:
        filename += '_' + s
    
    filename += '.txt'
    return filename


def search_for_related_trends(search_query: str = None):

    # current_date = datetime.datetime.now().strftime('%d_%m')

    if search_query is None:
        search_query = input("enter search query: ")
    
    # filename = set_file_name(search_query)

    referer = set_referer(search_query)

    print(f'{referer=}')

    # # Example usage:
    # search_word = "sanathan dharma"
    twitter_search_url = generate_twitter_search_url(search_query)
    # print(f'{twitter_search_url=}')

    search_tweet_meta = search_tweets(search_query, twitter_search_url=twitter_search_url, referer=referer)
    return [search_tweet_meta]


# search_for_related_trends()