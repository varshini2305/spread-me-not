# python parser/search_result_parser.py
import json
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import sys
import os
import logging

root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_directory)


def extract_info_recursive(data, paths, result=None):
    if result is None:
        result = {}  # Initialize the result dictionary if it's not provided

    current_level = data
    for key in paths:
        if key in current_level.keys():
            current_level = current_level[key]
            if key == 'instructions':
                current_level = current_level[0]
                if 'entries' in current_level.keys():
                    current_level = current_level['entries']
            print(key)
        else:
            # Key not found, stop processing
            return result

    # Once all keys in the path are found, extract the information
    result = current_level
    return result

def filter_irrelevant_keys(key, d):
    print(f"{key=}, {d.keys()=}")
    
    if key == 'tweets_info' and 'entities' in d.keys():
        del d['entities']
    if key == 'tweets_info' and 'extended_entities' in d.keys():
        del d['extended_entities']
    

    return d




def extract_attr_recursive(data, paths, key):
    """
    Recursively extract attributes from a nested dictionary based on the specified paths.

    Args:
        data (dict): The nested dictionary to extract attributes from.
        paths (list): List of keys representing the path to the desired attributes.
        result (dict): Dictionary to store the extracted attributes (optional).

    Returns:
        dict: Extracted attributes as a dictionary.
    """

    result = {}  # Initialize the result dictionary if it's not provided

    current_level = data
    for key in paths:
        try:
            if key in current_level.keys():
                current_level = current_level[key]
            else:
                # Key not found, stop processing
                return result, 0
        except Exception:
            print(f"{current_level=}")
            exit(0)

    # Once all keys in the path are found, extract the information

    
    return current_level, 1


'''
input_file = 'data/search_query_compilation.json'
output_json_file = 'data/formatted_search_results.json'
output_pickle_file = 'data/formatted_search_results.pkl'
'''
def process_data(input_file: str = 'data/search_query_compilation.json', 
                 output_json_file: str = 'data/formatted_search_results.json', 
                 output_pickle_file: str = 'data/formatted_search_results.pkl' , data: list = None):
    """
    Load JSON data, extract specified attributes, and store the results in JSON and Parquet formats.

    Args:
        input_file (str): Path to the input JSON file.
        output_json_file (str): Path to the output JSON file for formatted data.
        output_pickle_file (str): Path to the output Parquet file for formatted data.
    """
    if data is None:
        limit = False
        with open(input_file, 'r') as file:
            data = json.load(file)
    else:
        limit = True

    search_results_combined = []

    for doc in data:
        search_result_meta = {
            'search_query': doc['search_query'],
            'search_date': doc['search_date'],
            'no_of_results': None,
            'search_results': {}
        }
        try:
            if 'entries' in doc['search_results']['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][0].keys():
                search_result_meta['search_results']['result_type'] = 'user' if doc['search_results']['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][0]['entries'] == 'TimelineTimelineModule' else 'tweet'

                entries = extract_info_recursive(doc, paths_to_extract)

                parsed_entries = []

                for entry in entries:
                    parsed_entry = {}
                    valid = 1
                    for key, value in attributes_to_extract.items():
                        attributes_meta, valid = extract_attr_recursive(entry, value, key)
                        attributes_meta = filter_irrelevant_keys(key, attributes_meta)
                        parsed_entry[key] = attributes_meta
                        valid *= valid

                    if valid == 1:
                        if not(parsed_entry['tweets_info'] == {} or parsed_entry['user_profile_meta'] == {}):
                            parsed_entries.append(parsed_entry)

                if limit is True:
                    search_result_meta['search_results']['parsed_results'] = parsed_entries[:10]
                else:
                    search_result_meta['search_results']['parsed_results'] = parsed_entries[:10]
                    
                search_result_meta['search_results']['result_count'] = len(parsed_entries)
        
        except KeyError:
            logging.exception(f"traceback: {doc=}")
        

        search_results_combined.append(search_result_meta)

    # Save the formatted data as a JSON file
    with open(output_json_file, 'w') as json_file:
        json.dump(search_results_combined, json_file, indent=4)

    # Convert the formatted data to a Pandas DataFrame
    df = pd.DataFrame(search_results_combined)
    df.to_pickle(output_pickle_file)

    
    return search_results_combined

# Define paths and attributes to extract
paths_to_extract = [
    'search_results',
    'data',
    'search_by_raw_query',
    'search_timeline',
    'timeline',
    'instructions'
]

attributes_to_extract = {
    'tweets_info': ['content', 'itemContent', 'tweet_results', 'result', 'legacy'],
    'hashtag_used': ['content', 'itemContent', 'tweet_results', 'result', 'legacy', 'entities', 'hashtags'],
    'user_profile_meta': ['content', 'itemContent', 'tweet_results', 'result', 'core', 'user_results', 'result', 'legacy'],
    'client_event_info': ['content', 'clientEventInfo']
    # 'additional_entities': ['content', 'itemContent', 'tweet_results', 'result', 'legacy', 'entities']
}

# Specify the input and output file paths
input_file = 'data/search_query_compilation.json'
output_json_file = 'data/formatted_search_results.json'
output_pickle_file = 'data/formatted_search_results.pkl'

# Process the data and save it in the specified formats
# process_data(input_file, output_json_file, output_pickle_file)
