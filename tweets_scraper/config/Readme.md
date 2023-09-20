## How to fetch Auth info and cURL used for Trending tweets, and search requests in Twitter?


Trending tweets  - 

1. Login to your personal twitter account

2. If you plan to fetch all the trending tweets displayed in the trending tab of your feed, open the explore tab, 
open the inspect element, clear the network log, then click on trending tab, and then within 1-2 seconds stop recording the network activity (to overcrowding requests info in the network log), to only locate the API request used to fetch the trending tweets on the page

3. Copy as cURL - for the guides.json (in this case), basically search for a specific GET request which has the response json of the displayed tweets/hashtags

4. paste the cURL in Postman and fetch response (you must be able to get the response meta), copy Python-Requests format for the cURL, then use it in python for scraping accordingly


Things to note - 

1. Since, the results are updated only with time, and is not specific to any search term, referer - https://twitter.com/explore/tabs/trending

2. Similarly, url used also does not usually change, 

3. headers like - x-client-transaction-id, x-client-uuid, x-csrf-token, cookie, authorization - are subject to change with every user session






```
curl 'https://twitter.com/i/api/2/guide.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&include_ext_is_blue_verified=1&include_ext_verified_type=1&include_ext_profile_image_shape=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_ext_limited_action_results=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_ext_views=true&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&tab_category=objective_trends&count=20&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2CbirdwatchPivot%2CsuperFollowMetadata%2CunmentionInfo%2CeditControl' \
  -H 'authority: twitter.com' \
  -H 'accept: */*' \
  -H 'accept-language: en-GB,en;q=0.5' \
  -H 'authorization: ******' \
  -H 'cookie: ******'' \
  -H 'referer: https://twitter.com/explore/tabs/trending' \
  -H 'sec-ch-ua: ******' \
  -H 'sec-ch-ua-mobile: ******' \
  -H 'sec-ch-ua-platform: ******'' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-gpc: 1' \
  -H 'user-agent: ******'' \
  -H 'x-client-transaction-id: ******'' \
  -H 'x-client-uuid: ******'' \
  -H 'x-csrf-token: ******'' \
  -H 'x-twitter-active-user: yes' \
  -H 'x-twitter-auth-type: OAuth2Session' \
  -H 'x-twitter-client-language: en' \
  -H 'x-twitter-utcoffset: +0530' \
  --compressed
```


How does things change if I want to scrape search tweets - 

1. Go to the search bar and type the query, 

2. before pressing enter to search, open inspect tool, clear this existing network log, and press enter to search for the typed query, and quickly stop recording the network log after.

3. Locate the API get request used to fetch the information displayed on the twitter feed, you can quickly locate it by scanning through the response section of each of the requests, its usually XHR type.

4. Once you find the specific API request used to fetch the search results displayed in the feed, copy its cURL, and then paste in Postman, to fetch and check the response, if it works fine, copy the Python-Requests format of the same cURL, and do the necessary parsing of the response received.


```
curl --location 'https://twitter.com/i/api/graphql/3Ej-6N7xXONuEp5eJa1TdQ/SearchTimeline?variables=%7B%22rawQuery%22%3A%22wednesday%22%2C%22count%22%3A20%2C%22querySource%22%3A%22typed_query%22%2C%22product%22%3A%22Top%22%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D' \
--header 'authority: twitter.com' \
--header 'accept: */*' \
--header 'accept-language: en-GB,en;q=0.5' \
--header 'authorization: *************' \
--header 'content-type: application/json' \
--header 'cookie: ************' \
--header 'referer: https://twitter.com/search?q=wednesday&src=typed_query&f=top' \
--header 'sec-ch-ua: *******' \
--header 'sec-ch-ua-mobile: *******' \
--header 'sec-ch-ua-platform: *******' \
--header 'sec-fetch-dest: empty' \
--header 'sec-fetch-mode: cors' \
--header 'sec-fetch-site: same-origin' \
--header 'sec-gpc: 1' \
--header 'user-agent: *******' \
--header 'x-client-transaction-id: *******' \
--header 'x-client-uuid: *******' \
--header 'x-csrf-token: *******' \
--header 'x-twitter-active-user: yes' \
--header 'x-twitter-auth-type: OAuth2Session' \
--header 'x-twitter-client-language: en'
```


Things to note - 


1. Deeper understanding of type, initiator of the request is required
2. How to check for auth window - until with the auth token is valid and does not expire (< 1 day, and the user must be logged in, and if they log out and log back in the auth tokens and cookies will change)
3. what does the auth type of OAuth2Session mean
4. what are the headers like - x-client-transaction-id, x-client-uuid, x-csrf-token, cookie, authorization
5. usually the referrer - is modified based on the search query and the search words within a query separarted by space are separated by %20 in the referer URL, this might come in handy when you modify the header to make search specific requests
6. In the above case, even the url has the search query - so based on the format in which the search query occurs within the url, we can format the url used while making the request from python - for any specific search phrase.



### To understand more on what kind of scraping is allowed by terms and conditions of Twitter

1. check - https://twitter.com/robots.txt

2. Infer - the type of requests allowed by a useragent

3. Wait 1 second between successive requests. See ONBOARD-2698 for details.
   - Crawl-delay: 1
4. Independent of user agent. Links in the sitemap are full URLs using https:// and need to match - the protocol of the sitemap.
   - Sitemap: https://twitter.com/sitemap.xml  

5. Allowed requests - 
  - Allow: /hashtag/*?src=
  - Allow: /search?q=%23
  - Allow: /i/api/


### Things to do - 

1. Set up a script to use the username and password to fetch the auth config info on the fly, instead of manually updating the auth params

2. How or why cookies are used in the headers?

3. How to avoid being tracked when the scraping resembles a suspicious activity, IP address, user-agent info etc can be avoided being passed in the request body.