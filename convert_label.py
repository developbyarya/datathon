import pandas as pd

df = pd.read_csv("merapi_uncover_tweets_sample_with_annotation.csv")

print("Unique label:",df["annotation"].unique())

# convert to single label: kecelakaan

df["is_kecelakaan"] = df["annotation"].apply(lambda x: 1 if x == "kecelakaan" else 0)

print(df[["created_at", "text", "is_kecelakaan"]].head())

df.to_csv("100_merapi_uncover_sample_with_kecelakaan.csv", index=False)