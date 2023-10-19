import requests
import json

url = "https://twitter.com/i/api/graphql/lZ0GCEojmtQfiUQa5oJSEw/SearchTimeline?variables=%7B%22rawQuery%22%3A%22beheaded%20babies%20hamas%20until%3A2023-10-11%20since%3A2023-10-10%22%2C%22count%22%3A20%2C%22querySource%22%3A%22typed_query%22%2C%22product%22%3A%22Top%22%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22responsive_web_home_pinned_timelines_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"

# payload = {}
headers = {
  'authority': 'twitter.com',
  'accept': '*/*',
  'accept-language': 'en-GB,en;q=0.6',
  'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
  'content-type': 'application/json',
  'cookie': 'guest_id=v1%3A169761096643607003; guest_id_ads=v1%3A169761096643607003; guest_id_marketing=v1%3A169761096643607003; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCDKwf0GLAToMY3NyZl9p%250AZCIlYmE1NDM5NmJhYWNkNWYxMzY0MzNkNDk1OWNhYjJlNDI6B2lkIiUzZjc5%250AZWM0NWUxOGFlYWVjNTJjYjgxZTM5ZmNiMWNiMg%253D%253D--ff8ee2a763bb41f6f5aef2f9c1b000a46aa21932; kdt=Iw3OHnjtZii6SVH14wqjv36p2drDWTLMO8s74BXC; auth_token=f75fff955350f0d7bdf196865a27feac0707f06b; ct0=7207742517f86feb60150e4c3ca9a20f66439b5d2927604601c6117a1ba97879181e56ab824ded0bd7d3fea03b886b05beb15926cd5ea019a6ff5603b37f9275f3c4da7d0661b3db0d4f45d3bac28686; lang=en; twid=u%3D759797697679196160; att=1-YMyAwtLqreEkeCSS2POgTFdy4gysk0A4erHcJTAT; external_referer=8e8t2xd8A2w%3D|0|4abf247TNXg4Rylyqt4v49u2LWyy1%2FaFyfd602NkflM%3D; personalization_id="v1_nUsNXTEorRGYaDJIzuTpRw=="; guest_id=v1%3A169503345039396724; guest_id_ads=v1%3A169503345039396724; guest_id_marketing=v1%3A169503345039396724; personalization_id="v1_ALinYRN22ERohNAPygVTPg=="; twid=u%3D759797697679196160',
  # 'referer': 'https://twitter.com/search?lang=en&q=beheaded%20babies%20hamas%20until%3A2023-10-11%20since%3A2023-10-10&src=typed_query',
  # 'sec-ch-ua': '"Chromium";v="118", "Brave";v="118", "Not=A?Brand";v="99"',
  # 'sec-ch-ua-mobile': '?0',
  # 'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'sec-gpc': '1',
  # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
  'x-client-transaction-id': '6qMjFQS8S+HGUP9JB32frFJ2/1fB0ibR/DtmI3XIUMYHA8TJcW/jYom/Od2kc9Bi822NCupqtwNQJwJ4olZdzriUDmZj6w',
  'x-csrf-token': '7207742517f86feb60150e4c3ca9a20f66439b5d2927604601c6117a1ba97879181e56ab824ded0bd7d3fea03b886b05beb15926cd5ea019a6ff5603b37f9275f3c4da7d0661b3db0d4f45d3bac28686',
  'x-twitter-active-user': 'yes',
  'x-twitter-auth-type': 'OAuth2Session',
  'x-twitter-client-language': 'en'
}

response = requests.request("GET", url, headers=headers)

print(response.text)
