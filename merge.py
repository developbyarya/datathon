import pandas as pd

df_100 = pd.read_csv("100_merapi_uncover_sample_with_kecelakaan.csv")

df_naima = pd.read_csv("naima.csv", index_col=0)
df_naima_labeled = pd.read_csv("naima_labeled.csv", index_col=0)
df_naima_formated = df_naima.copy()
df_naima_formated['is_kecelakaan'] = df_naima_labeled['is_kecelakaan']
print("Miising target: ", df_naima_formated['is_kecelakaan'].isna().sum())
df_naima_formated.dropna(subset=['is_kecelakaan'], inplace=True)
df_naima_formated.reset_index(inplace=True)
print(df_naima_formated.head())


df_bintoro = pd.read_csv("bintoro_labeled.csv")
print(len(df_bintoro['created_at'].unique()))
df_all = pd.read_csv("merapi_uncover_tweets.csv")
print(len(df_all['created_at'].unique()))

df_all_labeled = pd.concat([df_100, df_naima_formated, df_bintoro])


print(len(df_all_labeled), "vs", len(df_all))

df_all_labeled[['created_at', 'text', 'is_kecelakaan']].to_csv("all_labeled.csv", index=False)