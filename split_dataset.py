import pandas as pd

df = pd.read_csv("merapi_uncover_tweets.csv")
df.set_index(["created_at", "text"], inplace=True)

print("Total len:",len(df))

df_sample_labeled = pd.read_csv("merapi_uncover_tweets_sample_with_annotation.csv")
df_sample_labeled.set_index(["created_at", "text"], inplace=True)

print("Labeled len:",len(df_sample_labeled))

df_not_labeled = df[~df.index.isin(df_sample_labeled.index)]
# decompose the index back to the original columns
df_not_labeled.reset_index(inplace=True)


print("Not labeled len:",len(df_not_labeled))

print("Not labeled sample:",df_not_labeled.head())

split_name = ["bintoro", "naima"]

# split the df_not_labeled into 2 parts
df_not_labeled_1 = df_not_labeled.iloc[:len(df_not_labeled)//2]
df_not_labeled_2 = df_not_labeled.iloc[len(df_not_labeled)//2:]

print("Not labeled 1 len:",len(df_not_labeled_1))
print("Not labeled 1 sample:",df_not_labeled_1.head())
print("Not labeled 2 len:",len(df_not_labeled_2))
print("Not labeled 2 sample:",df_not_labeled_2.head())

df_not_labeled_1.to_csv(f"{split_name[0]}.csv", index=False)
df_not_labeled_2.to_csv(f"{split_name[1]}.csv", index=False)
