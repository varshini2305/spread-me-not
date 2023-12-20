import re
import json
from bs4 import BeautifulSoup
from functools import lru_cache
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
import os
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file
_ = load_dotenv('/Users/varshinibalaji/Documents/DSProjects/chatgpt_prompting/config.env')



@lru_cache(maxsize=None)  # Set maxsize to None for an unbounded cache
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=0)
    return response.choices[0].message["content"]


def separate_claims(claim):
    prompt = f"""
    identify individual/independent claims from the given text, which needs individual evidence, or 
    if some statements have causal relation (meaning if A results in B, only claim A needs evidence
    individual_claims [list of independent claims that require separate evidence, sorted in the order of severity], dependent_claims - list of claims with a dependence on another independent claim being true  
    i.e if claim A is true implies B, then B is a dependent claim
    return: [individual_claims,dependent_claims]
    claim: {claim}
    """

    response = get_completion(prompt)
    # Define a regular expression pattern to extract individual claims
    pattern = r"\d+\.\s(.*?)(?=\d+\.|\Z)"  # This pattern captures text between numbers and stops at the next number or end of string

    # Use re.findall to find all matches in the input string
    individual_claims_matches = re.findall(pattern, response, re.DOTALL)

    # Print the list of individual claims
    print(individual_claims_matches)

    individual_claims = []

    for i in individual_claims_matches:
        individual_claims.append(i.strip('\n\ndependent_claims: \n'))
        if i.find('\ndependent_claims') != -1:
            break

    return individual_claims


def generate_search_keyword(claim):
    prompt = f"""
    Identify the individual claims made in the given text, 
    - extract keywords for each claim - that represents the main top being discussed,
    - return the top 3 keywords as a space separated string to search in a site  
    claim: '''{claim}'''
    return -> keyword_string
    """
    response = get_completion(prompt)
    return response


def verify_claim(tweet, similar_result):
    prompt = f"""
    Check if the given text is confirming or denying the claim, or if there is no sufficient information provided to verify the claim. 
    verification_status - 'valid', 'invalid' or 'unverified'
    brief - explain briefly why the claim is valid (if there is supporting evidence), invalid (if there is no evidence, or there is opposite evidence), unverified(if no sufficient info)
    claim: {tweet}, text: {similar_result}
    return: verification_status, brief
    """

    response = get_completion(prompt)
    return response


def most_similar_document(query, documents):
    if documents:
        # Combine the query and documents
        corpus = [query] + documents

        # Vectorize the text using TF-IDF
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(corpus)

        # Calculate cosine similarity between the query and documents
        cosine_similarities = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1:])

        # Find the most similar document
        most_similar_index = cosine_similarities.argmax()

        # Print the most similar document
        print(f"Query: {query}")
        print(f"Most Similar Document: {documents[most_similar_index]}")
        return documents[most_similar_index]
    else:
        return None


base_url = "https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=en&source=gcsc&gss=.com&cselibv=2b35e7a15e0e30e2&cx=006616930764067935488%3Aop0ec0xnjo8&safe=off&cse_tok=AB-tC_7RtpcVy4FppHGfms5JuvfB%3A1700204571091&sort=&exp=csqr%2Ccc%2Cdtsq-3&oq=beheaded+babies&callback=google.search.cse.api15031"


def set_query(query: str, url: str = base_url):
    query = query.replace(' ', '+')
    query = "&q=" + query
    url += query
    # print(f'{url=}')
    return url
    
from pymongo import MongoClient
from elasticsearch import Elasticsearch

import yaml

with open('config/auth.yaml') as f:
    mongo_info = yaml.safe_load(f)

connection_string = mongo_info['mongo_connection_uri']


def fetch_checked_facts(search_query):
    # Establish a connection to the MongoDB Atlas cluster
    client = MongoClient(connection_string)
    
    # Access the 'facts' database and 'fact_check_articles' collection
    db = client['facts']
    collection = db['fact_check_articles']
    
    # Define the aggregation pipeline for the search
    pipeline = [

        {
            '$search': {
                'index': 'article_search',
                'text': {
                    'query': search_query,
                    'path': 'processed_article'

                }
            }
        },
        {
            '$project': {
                '_id': 0,
                'processed_article': 1

            }
        }
    ]

    # Execute the aggregation pipeline
    result = list(collection.aggregate(pipeline))

    # Sort the result based on hitRate in descending order
    # result.sort(key=lambda x: x['hitRate'], reverse=True)

    # Return the top 2 or 3 documents
    return result[:3]

def fetch_real_time_article(processed_keyword):
    documents = []
    url = set_query(processed_keyword)
    print(f'{processed_keyword=}')

    payload = {}
    headers = {
        'authority': 'cse.google.com',
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.9',
        'referer': 'https://www.factcheck.org/',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'cross-site',
        'sec-gpc': '1',
        'user-agent': 'windows 11',
        'Cookie': 'NID=511=IWGsihXCmKb-AXoqUQ0yx-3tj5qK_1CKc00JCaR47VDKsWgGlpFo24LR8WHJqIK7WonmBdlGUgiJ_K1amuoxR8L8TS31aPskrwsGG0w4ytiB0TTrfkFCeDqB487TiOUcAF4OFGG3hwLX8VltthwIU7OPhd0qh28P0_DqNbuVzMQ'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = json.loads(response.text.strip('/*O_o*/\ngoogle.search.cse.api15031(').strip(');'))
    print(f"json_response - {json_response}")
    print(f"url - {url}")

    try:
        results = json_response['results']

        for r in results:
            url = r['formattedUrl']

            headers = {
                'Referer': 'https://www.factcheck.org/'
            }

            article = requests.request("GET", url, headers=headers, data=payload)
            article = article.text

            html_response = article

            # Parse the HTML content
            soup = BeautifulSoup(html_response, 'html.parser')

            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()  # rip it out

            query = {
                "query": {
                    "multi_match": {
                        "query": processed_keyword,
                        "fields": ["title", "content"],
                        "fuzziness": 2,
                    }
                }
            }

            documents = []
            paragraphs = soup.find_all("p")
            for index, paragraph in enumerate(paragraphs):
                text = paragraph.get_text()
                # document = {"id": index, "content": text}
                documents.append(text)
                print(text)
                print(f"{'*' * 20}")
            break
    except Exception:
        pass

    return documents


keywords = []
processed_keyword = ''

from keybert import KeyBERT
kw_model = KeyBERT()

def replace_non_alphanumeric(input_string):
    # Use a regular expression to replace non-alphanumeric characters with spaces
    cleaned_string = re.sub(r'[^a-zA-Z0-9]', ' ', input_string)
    return cleaned_string


def credibility_checker(x):
    independent_claims = separate_claims(x)
    global keywords, processed_keyword
    keywords = []
    claim_metas = []
    for i in independent_claims:
        # keyword = generate_search_keyword(i)
        # keywords.append(generate_search_keyword(i))
        keywords = kw_model.extract_keywords(i)
        words = []
        for w, s in keywords:
            words.append(w)
        processed_keyword = ' '.join(keywords)
        processed_keyword = replace_non_alphanumeric(processed_keyword)
        keyword = replace_non_alphanumeric(keyword)
        documents = fetch_checked_facts(keyword)
        match = most_similar_document(keyword, documents)
        claim_meta = verify_claim(x, match)
        print(f"{claim_meta=}")
        claim_metas.append({'claim': i, 'credibility': claim_meta})
    return claim_metas


@lru_cache(maxsize=None)
def check_tweet_emotion_verify_facts(x):
    prompt = f"""
    Check if the text has triggering content, controversial, anger, hatred emotion, and 
    classify it as neutral, mildly triggering or extremely triggering - based on the tone and words used in the text.
    then, extract list of keywords (non-generic) from text that well represent the main topic or claim discussed.
    keyword_string - form a single keyword string concatenating all keywords separated by space
    return: [trigger_numeric_code, trigger_type, keyword_string, keywords, brief]
    Review text: '''{x}'''
    """

    response = get_completion(prompt)

    tweet_type = response[0]

    if tweet_type != 0:  # 0 -> neutral or not triggering
        credibility_meta = credibility_checker(x)
    else:
        credibility_meta = None

    return credibility_meta


# credibility_meta = check_tweet_emotion_verify_facts(tweet)