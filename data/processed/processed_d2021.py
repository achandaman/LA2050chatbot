import pandas as pd
import json
import re
import matplotlib.pyplot as plt
import os
#from elasticsearch import Elasticsearch
from IPython.display import display
with open(r'/Org_data.json',encoding='utf-8') as p:
    Org_data = json.load(p)
with open(r'/data_2021.json',encoding='utf-8') as f:
    data_2021 = json.load(f)


# Use pd.json_normalize to convert the JSON to a DataFrame
df_org = pd.json_normalize(Org_data)
#df = pd.json_normalize(data)
df_21 = pd.json_normalize(data_2021)


df_21.columns = ['Title', 'Slug', 'Year', 'Organization', 'Description', 'Goal', 'Ranking', 
                   'Project Description', 'Stage of Innovation', 'Evidence of Success', 
                   'Problem Statement', 'Additional Goals', 'Working Areas in LA', 
                   'Impact on LA', 'People Impacted', 'Live Metrics', 'Connect Metrics', 
                   'Collaborations', 'Learn Metrics', 'Play Metrics', 'Create Metrics']

# Combine the metric columns into one "Impact Metrics" column
df_21['Impact Metrics'] = df_21[['Live Metrics', 'Connect Metrics', 'Learn Metrics', 'Play Metrics', 'Create Metrics']].apply(lambda x: ', '.join(x.dropna()), axis=1)

# Optionally, drop the individual metric columns after combining
df_21.drop(['Live Metrics', 'Connect Metrics', 'Learn Metrics', 'Play Metrics', 'Create Metrics'], axis=1, inplace=True)

#print(df_21.columns)


df_org.columns = ['Slug', 'Status', 'Website', 'Instagram', 'Twitter', 'FaceBook', 'Newsletter', 'Title', 'IRS Standing', 'Zipcode', 'Volunteer', 'Summary', 'Category']
df_21 = df_21.drop(['Ranking'], axis=1)


df_21 = df_21.fillna('Working Individually')
df_21['Collaborations'].fillna('Working Individually', inplace=True)
df_org = df_org.fillna('N/A')
df_21['People Impacted'].fillna('Not Applicable', inplace=True)



def extract_direct_impact(text):
     match = re.search(r'Direct Impact: ([\d,]+\.?\d*)', text)
     if match:
        return float(match.group(1).replace(',', ''))  # Remove commas and convert to float
     return None

df_21['People Impacted'] = df_21['People Impacted'].apply(extract_direct_impact)
df_org = df_org.drop_duplicates(subset='Title')
final_List= df_21.merge(df_org , left_on='Organization', right_on= 'Title', how='inner')
final_List = final_List.drop(['Slug_y', 'Title_y'],axis = 1)
final_List = final_List.fillna(0)

#print(df_21.info())

df_21.to_csv('output_data_21.csv', index=False)