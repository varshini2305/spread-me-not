# streamlit run fetch_viral_tweets.py
import sys
import os


# Add the path to the root directory to the Python path
root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_directory)

import fetch_trending_tweets_of_the_day as top_trends
import search_query_tweets as trend_searcher

from parser import search_result_parser as search_parser
from parser import trending_meta_parser as trend_parser


import streamlit as st
import pandas as pd

def display_search_results(parsed_results: list = None):
    # parsed_results = results['search_results']['parsed_results']
    # result_type = result['search_results']['result_type']
    # st.write(parsed_results)
    print(f"{type(parsed_results)=}, {len(parsed_results)=}")
    # Create a DataFrame for easier manipulation
    df_list = []
    for res in parsed_results:
        result = res['search_results']['parsed_results']
        # print(f"{result.keys()=}")
        for each in result:
            tweet_info = each["tweets_info"]
            user_profile = each["user_profile_meta"]
            result_type = each['client_event_info']['element']
            
            # Append data to DataFrame
            df_list.append({
                "Full Text": tweet_info.get("full_text"),
                "Favorite Count": tweet_info.get("favorite_count"),
                "Reply Count": tweet_info.get("reply_count"),
                "Retweet Count": tweet_info.get("retweet_count"),
                "User Name": user_profile.get("name"),
                "Followers Count": user_profile.get("followers_count"),
                "Location": user_profile.get("location"),
                "Verified": user_profile.get("verified"),
                "User Favorite Count": user_profile.get("favourites_count"),
                
                "Created At": tweet_info.get("created_at"),
                'result_type': result_type
            })

    # Create a DataFrame
    df = pd.DataFrame(df_list)

    # Streamlit app
    # st.title("Twitter Data Visualization")

    # Display the data table
    st.dataframe(df)


# Define your function to process non-empty search queries
def process_search_query(search_query):
    search_tweet_meta = trend_searcher.search_for_related_trends(search_query)
    parsed_results = search_parser.process_data(data=search_tweet_meta)
    display_search_results(parsed_results)



def display_top_trends(trending_topics: list):
    # Create a DataFrame
    df = pd.DataFrame(trending_topics)

    # Streamlit app
    st.title("Top Trending Tweets")

    # Display the top trending tweets in a table
    st.table(df[['name', 'category', 'rank', 'post_count', 'related_terms']])

    # st.write(trending_topics)


def handle_empty_query():
    trending_topics = top_trends.trending_meta_parser()
    display_top_trends(trending_topics)
    

# Streamlit app
def main():
    st.title("TrendSearcher - What's trending on Twitter?")
    
    # Create a text input box for the search query
    search_query = st.text_input("Enter a search query:")
    
    # Create a search button
    if st.button("Search"):
        if search_query:
            # Call the function for no  n-empty search queries
            result = process_search_query(search_query)
            # st.write(result)
        else:
            # Call the function for empty queries
            result = handle_empty_query()
            # st.write(result)
    if st.button("Get Latest Trends"):
        result = handle_empty_query()


main()