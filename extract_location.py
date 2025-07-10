import pandas as pd
import json
df = pd.read_csv("location-raw.csv")

clean_df = pd.DataFrame()

clean_df[['created_at', 'text']] = df[['created_at', 'text']].copy()

for index, row in df.iterrows():
    try:
        label = row['label']
        label_dict = json.loads(label)
        location_result = [item.get('text') for item in label_dict]
        print(location_result)
        clean_df.loc[index, 'location'] = json.dumps(location_result)
    except Exception as e:
        print(row['label'])
        print("error: ", e)
        # break
    # break

print(clean_df.head())
clean_df.to_csv("kecelakaan-with-location-raw.csv", index=False)
