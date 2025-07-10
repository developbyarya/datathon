import pandas as pd

df = pd.read_csv('merapi_uncover_tweets.csv')

print(df.head())

df = df.sample(n=100)

df.to_csv('merapi_uncover_tweets_sampled.csv', index=False)