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
import json

import sys
import os
root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_directory)

from parser.trending_meta_parser import trending_meta_parser
# Email ID scraping from twitter accounts
# # auth info

with open('config/auth.yaml', 'r') as file:
    trends_config = yaml.safe_load(file)

authorization = trends_config['authorization']
x_client_transaction_id = trends_config['x_client_transaction_id']
x_client_uuid = trends_config['x_client_uuid']
x_csrf_token =  trends_config['x_csrf_token']
cookie = trends_config['cookie']

def explore_trends():
        

        url = "https://twitter.com/i/api/2/guide.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&include_ext_is_blue_verified=1&include_ext_verified_type=1&include_ext_profile_image_shape=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_ext_limited_action_results=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_ext_views=true&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&tab_category=objective_trends&count=20&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2CbirdwatchPivot%2CsuperFollowMetadata%2CunmentionInfo%2CeditControl"

        payload = {}
        headers = {
        'authority': 'twitter.com',
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.9',
        'authorization': authorization,
        'cookie': cookie,
        'referer': 'https://twitter.com/explore/tabs/trending',
        # 'sec-ch-ua': '"Brave";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        # 'x-client-transaction-id': x_client_transaction_id,
        # 'x-client-uuid': x_client_uuid,
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
        # print(formatted_json)

        # # Open the text file in append mode
        # with open(file_name, 'w') as file:
        #     # Parse the JSON string into a Python dictionary
        #     file.write(formatted_json + '\n')
        
        

        # New entry
        loaded_json_data = dict()
        loaded_json_data['date'] = datetime.datetime.now().strftime('%d-%m-%Y')
        loaded_json_data['trends_meta'] = parsed_json
        

        # Read the existing JSON file
        try:
            with open('data/trending_tweets_compilation.json', 'r') as file:
                data = json.load(file)
            
            print(f"{type(data)=}, {len(data)=}")
            # print(f"{data=}")
            # Find the index of an existing entry with the same date or -1 if not found
            new_data = data.copy()
            match_doc = -1
                
            # print(f"{type(data)=}")
            # print(f"{data=}")
            # Find the index of an existing entry with the same date or -1 if not found
            
            for index, doc in enumerate(data):
                # print(f"{doc=}")
                if doc['date'] == loaded_json_data["date"]:
                    # Overwrite the existing entry with the same date
                    new_data[index]['trends_meta'] = parsed_json
                    match_doc = 1
                    break
                    
                # as a matching doc with same search query and on the same date already found and updated
                
        
            if match_doc == -1:
                # If no match is found, append the new entry
                print(f"{loaded_json_data['date']=}")
                
                new_data.append(loaded_json_data)
                

            # Write back to the JSON file
            with open('data/trending_tweets_compilation.json', 'w') as file:
                json.dump(new_data, file)
                    

            with open('data/trending_tweets_compilation.json', 'r') as file:
                data = json.load(file)
                no_of_dates_stored = len(data)
                print(f"{type(data)=}, {no_of_dates_stored=}")


        except FileNotFoundError:
            with open('data/trending_tweets_compilation.json', 'a') as json_file:
                loaded_json_data_list = [loaded_json_data]
                json.dump(loaded_json_data_list, json_file)


# Get the current date in the format dd_mm
# current_date = datetime.datetime.now().strftime('%d_%m')
# file_name = f'data/trending_tweets_{current_date}.txt'



# explore_trends()
