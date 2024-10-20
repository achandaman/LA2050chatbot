import pandas as pd
import json
import re
import matplotlib.pyplot as plt
import os
#from elasticsearch import Elasticsearch
from IPython.display import display

org_data_path = '../raw/organizations-new.json'
data_2020_path = '../raw/idea-2020-new.json'

with open(org_data_path,encoding='utf-8') as org_file:
    org_data = json.load(org_file)
with open(data_2020_path,encoding='utf-8') as data_2020_file:
    data_2020 = json.load(data_2020_file)


# Use pd.json_normalize to convert the JSON to a DataFrame
df_org = pd.json_normalize(org_data)
df_20 = pd.json_normalize(data_2020)

# Rename the columns for clarity
df_org.columns = ['Slug', 'Status', 'Website', 'Instagram', 'Twitter', 'FaceBook', 'Newsletter', 'Title', 'IRS Standing', 'Zipcode', 'Volunteer', 'Summary', 'Category']
df_20.columns = [
    'Title', 'Slug', 'Year', 'Organization', 'Description', 'Goal', 'Ranking',
    'Impacted People', 'PLAY Metrics', 'Other LA2050 Goals', 
    'Innovation Stage', 'Success Definition', 'Valuable Resources', 
    'Work Areas', 'Collaboration Roles', 'Project Need', 
    'Org Importance', 'Impact', 'LEARN Metrics', 
    'LIVE Metrics', 'CREATE Metrics', 'COVID-19 Impact', 
    'Collaborating Organizations', 'CONNECT Metrics', 
    'Impacted People', 'Org Importance'
]

df_20 = df_20.drop(['Ranking'], axis=1)
df_20 = df_20.fillna('Working Individually')
df_org = df_org.fillna('N/A')



def extract_direct_impact(text):
    match = re.search(r'Direct Impact: ([\d,]+\.?\d*)', text)
    if match:
        return float(match.group(1).replace(',', ''))  # Remove commas and convert to float
    return None

df_20['Impact'] = df_20['Impact'].apply(extract_direct_impact)
df_org = df_org.drop_duplicates(subset='Title')
final_List= df_20.merge(df_org , left_on='Organization', right_on= 'Title', how='inner')
final_List = final_List.drop(['Slug_y', 'Title_y'],axis = 1)
final_List = final_List.fillna(0)
  

#es = Elasticsearch(
 #   ['http://localhost:9200'],  # Replace with your local Elasticsearch URL
 #   basic_auth=('elastic', '123456')  # Use your Elasticsearch password here
#)
#for index, row in final_List.iterrows():
 #   doc = row.to_dict()
    # Ensure that the document doesn't contain NaN or other problematic values
   # if None not in doc.values():  # Check if there are any None values
   #     try:
   #         es.index(index='nonprofit_data', id=index, document=doc)
   #     except Exception as e:
   #         print(f"Error indexing document with ID {index}: {e}")
   # else:
   #     print(f"Document with ID {index} contains None values and will not be indexed.")

