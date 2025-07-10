import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import pandas as pd
import asyncio
import random
from twikit import Client

USERNAME = 'merapi_uncover'
MAX_TWEETS = 1000

async def main():
    client = Client('en-US')
    

    if os.path.exists('cookies.json'):
        client.load_cookies(path='cookies.json')
    else:
        await client.login(
            auth_info_1='WeTeachMachine',
            # auth_info_2='weteachmachine@gmail.com',
            password='wtm-forfuture05'
        )
        client.save_cookies('cookies.json')

    user = await client.get_user_by_screen_name(USERNAME)

    tweets_to_store = []
    tweets = await user.get_tweets('Tweets', count=MAX_TWEETS)

    while len(tweets_to_store) < MAX_TWEETS and len(tweets) > 0:
        for tweet in tweets:
            tweets_to_store.append({
                'created_at': tweet.created_at,
                'text': tweet.full_text if hasattr(tweet, 'full_text') else tweet.text
            })
            if len(tweets_to_store) >= MAX_TWEETS:
                break
        try:
            await asyncio.sleep(random.uniform(1, 3))
            tweets = await tweets.next()
        except Exception:
            break

    df = pd.DataFrame(tweets_to_store)
    df.to_csv(f'{USERNAME}_tweets.csv', index=False)
    print(f'Saved {len(df)} tweets to {USERNAME}_tweets.csv')

asyncio.run(main()) 