import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.DataFrame(pd.read_json("final_filtered_data.json"))

train_df, test_df = train_test_split(df, test_size=0.27, random_state=42)

train_df.to_csv("train.csv", index=False, encoding="utf-8")
test_df.to_csv("test.csv", index=False, encoding="utf-8")