import json
import pandas as pd

filename = "project-1-at-2025-07-08-15-07-24aad610"
with open(f"{filename}.json", 'r') as f:
    data = json.load(f)

df = pd.DataFrame()

error_id = []

# iterate over the data json dict
for d in data:
    try:
        annot_data = d.get("data")
        annot_result = d.get("annotations")[0].get("result")[0].get("value").get("choices")[0]
        # print(annot_result)
        # merge annot data and annot result into one dict
        merged_dict = {**annot_data, "annotation": annot_result}
        # convert the merged dict to a pandas dataframe
        df = pd.concat([df, pd.DataFrame([merged_dict])], ignore_index=True)
    except IndexError as e:
        error_id.append(d.get("id"))
        print("Error on data: ")
        print(annot_data)
        print(d.get("annotations"))
        print(e)
       
  

print(error_id)
print(df.head())    
export_filename = "merapi_uncover_tweets_sample_with_annotation.csv"
df.to_csv(f"{export_filename}", index=False)
