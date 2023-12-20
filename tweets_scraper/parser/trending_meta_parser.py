'''
parse and fetch only the essential metadata about the trending tweets, in the required format

format of the sample response - refer to data/trending_tweets_20_09.txt

fetch trending tweets date wise data - data/trending_data

~ 60 tweets in the response json


'''
# python parser/trending_meta_parser.py

import json
import pandas as pd
import sys
import os
import fetch_trending_tweets_of_the_day as recent_trends

import datetime

root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_directory)


def load_trending_tweets(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def extract_trending_items(data):
    last_fetched_trends = data[-1]
    trending_items = last_fetched_trends['trends_meta']['timeline']['instructions'][1]['addEntries']['entries'][1]['content']['timelineModule']['items']
    return trending_items

# Function to convert a datetime object to Unix timestamp
def convert_to_unix_timestamp(date):
    return int(date.timestamp())
    

def extract_trend_info(trend, date):
    trend_info = {
        'date': date
    }
    try:
        trend_info['name'] = trend['item']['content']['trend']['name']
    except KeyError:
        trend_info['name'] = None

    try:
        trend_info['post_count'] = trend['item']['content']['trend']['trendMetadata']['metaDescription']
    except KeyError:
        trend_info['post_count'] = None

    try:
        trend_info['category'] = trend['item']['content']['trend']['trendMetadata']['domainContext']
    except KeyError:
        trend_info['category'] = None

    try:
        trend_info['rank'] = trend['item']['content']['trend']['rank']
    except KeyError:
        trend_info['rank'] = None

    try:
        trend_info['display_position'] = trend['item']['clientEventInfo']['details']['guideDetails']['transparentGuideDetails']['trendMetadata']['position']
    except KeyError:
        trend_info['display_position'] = None

    try:
        trend_info['related_terms'] = trend['item']['clientEventInfo']['details']['guideDetails']['transparentGuideDetails']['trendMetadata']['relatedTerms']
    except KeyError:
        trend_info['related_terms'] = None

    try:
        trend_info['topic_ids'] = trend['item']['clientEventInfo']['details']['guideDetails']['transparentGuideDetails']['trendMetadata']['topicIds']
    except KeyError:
        trend_info['topic_ids'] = None

    try:
        trend_info['cluster_id'] = trend['item']['clientEventInfo']['details']['guideDetails']['transparentGuideDetails']['trendMetadata']['clusterId']
    except KeyError:
        trend_info['cluster_id'] = None

    return trend_info



def format_post_count(post_count):
    if post_count:
        post_count = post_count.split(' posts')[0].replace(',', '')
        if 'K' in post_count:
            post_count = float(post_count.replace('K', '')) * 1000
        try:
            return float(post_count)
        except Exception:
            return 0.0
    return None

def format_tuple_terms(x):
    if x:
        return x[0]
    return None

def extract_and_format_trend_type(category):
    if 'Trending' in category:
        trend_type = category.split(' · ')[0]
        if trend_type == 'Only on Twitter':
            trend_type = 'twitter trending'
        return trend_type.lower()
    return category

def trending_meta_parser():
    
    data = load_trending_tweets('data/trending_tweets_compilation.json')
    
    trending_items = extract_trending_items(data)
    
    date = data[-1]['date']
    
    trends_meta = []

    
    current_datetime = datetime.datetime.now()

    # Format the current date as a string
    current_date = current_datetime.strftime("%d-%m-%Y")

    if date != current_date:
        # update with latest trends from present day
        recent_trends.explore_trends()
    
    data = load_trending_tweets('data/trending_tweets_compilation.json')
    
    trending_items = extract_trending_items(data)
    
    date = data[-1]['date']
    
    for trend in trending_items:
        trend_info = extract_trend_info(trend, date)
        trends_meta.append(trend_info)
    
    trends_df = pd.DataFrame(trends_meta)
    
    trends_df['post_count'] = trends_df['post_count'].apply(format_post_count)
    trends_df['related_terms'] = trends_df['related_terms'].apply(format_tuple_terms)
    trends_df['topic_ids'] = trends_df['topic_ids'].apply(format_tuple_terms)
    trends_df['cluster_id'] = trends_df['cluster_id'].apply(format_tuple_terms)
    
    trends_df['category'] = trends_df['category'].apply(extract_and_format_trend_type)
    
    trends_df_formatted = trends_df[['date', 'name', 'category', 'rank', 'post_count', 'related_terms', 'topic_ids', 'cluster_id']]
    trends_df_formatted.columns = ['date', 'name', 'category', 'rank', 'post_count', 'related_terms', 'topic_ids', 'cluster_id']
    
    # Save the formatted data as a JSON file
    trends_records = trends_df_formatted.to_dict("records")
    with open('data/formatted_trends_compilation.json', 'w') as json_file:
        json.dump(trends_records, json_file, indent=4)
    
    trends_df_formatted.to_parquet("data/trending_tweets_meta.pq")

    # return top trends sorted by latest on top
    # Convert the 'date' column to datetime format
    trends_df_formatted['date_stamp'] = pd.to_datetime(trends_df_formatted['date'], format='%d-%m-%Y')

    

    # Apply the function to each row in the DataFrame to calculate Unix timestamps
    trends_df_formatted['unix_date'] = trends_df_formatted['date_stamp'].apply(convert_to_unix_timestamp)

    trends_df_formatted.sort_values(by = ['unix_date', 'post_count'], ascending=[False, False], inplace=True)

    top_trends = trends_df_formatted.to_dict("records")[:10]

    return top_trends


# trending_meta_parser()

