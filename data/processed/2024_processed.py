import pandas as pd
import json
import re
import matplotlib.pyplot as plt
import os
from elasticsearch import Elasticsearch
from IPython.display import display
with open(r'C:\Users\Andrew\Downloads\organizations-new.json',encoding='utf-8') as p:
    Org_data = json.load(p)
with open(r'C:\Users\Andrew\hello\idea-2024-new.json',encoding='utf-8') as f:
    data = json.load(f)
with open(r'C:\Users\Andrew\Downloads\idea-2022-new.json', encoding = 'utf-8') as k:
    data_2022 = json.load(k)

# Use pd.json_normalize to convert the JSON to a DataFrame
df_org = pd.json_normalize(Org_data)
df = pd.json_normalize(data)
df_22 = pd.json_normalize(data_2022)

# Rename the columns for clarity
df_22.columns = ['Title', 'Slug','Year', 'Organization', 'Description', 'Goal','Ranking', 'Mission Statement', 'Progression','End Goal','Quota', 'Support Statement', 'Project' ,'Impact','Location','Collaborations', 'Companies']
df.columns = ['Title', 'Slug', 'Year', 'Organization', 'Description', 'Goal', 'Ranking', 'Progression', 'Mission Statement', 'End Goal', 'Quota', 'Support Statement', 'Project', 'Impact', 'Collaborations']
df_org.columns = ['Slug', 'Status', 'Website', 'Instagram', 'Twitter', 'FaceBook', 'Newsletter', 'Title', 'IRS Standing', 'Zipcode', 'Volunteer', 'Summary', 'Category']
df = df.drop(['Ranking'], axis=1)
df_22 = df_22.fillna('N/A')
df = df.fillna('Working Individually')
df_org = df_org.fillna('N/A')



def extract_direct_impact(text):
    match = re.search(r'Direct Impact: ([\d,]+\.?\d*)', text)
    if match:
        return float(match.group(1).replace(',', ''))  # Remove commas and convert to float
    return None

df['Impact'] = df['Impact'].apply(extract_direct_impact)
df_org = df_org.drop_duplicates(subset='Title')
final_List= df.merge(df_org , left_on='Organization', right_on= 'Title', how='inner')
final_List = final_List.drop(['Slug_y', 'Title_y'],axis = 1)
final_List = final_List.fillna(0)
  

es = Elasticsearch(
    ['http://localhost:9200'],  # Replace with your local Elasticsearch URL
    basic_auth=('elastic', '123456')  # Use your Elasticsearch password here
)
for index, row in final_List.iterrows():
    doc = row.to_dict()
    # Ensure that the document doesn't contain NaN or other problematic values
    if None not in doc.values():  # Check if there are any None values
        try:
            es.index(index='nonprofit_data', id=index, document=doc)
        except Exception as e:
            print(f"Error indexing document with ID {index}: {e}")
    else:
        print(f"Document with ID {index} contains None values and will not be indexed.")

