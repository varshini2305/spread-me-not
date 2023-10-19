import requests
import json

url = "https://api.twitter.com/graphql/G3KGOASz96M-Qu0nwmGXNg/UserByScreenName?variables=%7B%22screen_name%22%3A%22dissocialspace%22%2C%22withSafetyModeUserFields%22%3Atrue%7D&features=%7B%22hidden_profile_likes_enabled%22%3Atrue%2C%22hidden_profile_subscriptions_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22subscriptions_verification_info_is_identity_verified_enabled%22%3Atrue%2C%22subscriptions_verification_info_verified_since_enabled%22%3Atrue%2C%22highlights_tweets_tab_ui_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%7D&fieldToggles=%7B%22withAuxiliaryUserLabels%22%3Afalse%7D"

payload = {}
headers = {
  'authority': 'api.twitter.com',
  'accept': '*/*',
  'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
  'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
  'content-type': 'application/json',
  'cookie': '_ga=GA1.2.986194487.1697629890; _gid=GA1.2.1898282474.1697629890; guest_id=v1%3A169762989087231874; guest_id_marketing=v1%3A169762989087231874; guest_id_ads=v1%3A169762989087231874; personalization_id="v1_QhhP6CtOK/hTe6icBgwgGw=="; gt=1714610262639346151; guest_id=v1%3A169503345039396724; guest_id_ads=v1%3A169503345039396724; guest_id_marketing=v1%3A169503345039396724; personalization_id="v1_ALinYRN22ERohNAPygVTPg=="; twid=u%3D759797697679196160',
  'origin': 'https://twitter.com',
  'referer': 'https://twitter.com/',
#   'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
#   'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
#   'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
  'x-client-transaction-id': 'wMpsM7pbRLAuEk5xkv7EUtw5Jy/pvsyPpQtyoYk/lqR+xDtxRpIBFL+qEjaLrQvXH66jIMAfcjI0VzyVutN0x4FvZYhGwQ',
  'x-guest-token': '1714610262639346151',
  'x-twitter-active-user': 'yes',
  'x-twitter-client-language': 'en-GB'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
