import pandas as pd
import json
import re
import matplotlib.pyplot as plt
import os
#from tabulate import tabulate
#from elasticsearch import Elasticsearch
from IPython.display import display
with open(r'/Org_data.json',encoding='utf-8') as p:
    Org_data = json.load(p)
with open(r'/data_2023.json',encoding='utf-8') as f:
    data_2023 = json.load(f)


# Use pd.json_normalize to convert the JSON to a DataFrame
df_org = pd.json_normalize(Org_data)
#df = pd.json_normalize(data)
df_23 = pd.json_normalize(data_2023)


#df_23.columns = ['Title', 'Slug', 'Year', 'Organization', 'Description', 'Goal', 'Ranking', 'Progression', 'Mission Statement', 'End Goal', 'Quota', 'Support Statement', 'Project', 'Impact', 'Collaborations']
df_23.columns = ['Title', 'Slug', 'Year', 'Organization', 'Description', 'Goal', 'Ranking',
                 'Issue Understanding','Stage of Innovation', 'Project Description',
                   'Impact on LA', 'Working Areas in LA',  'Evidence of Success',
                   'Primary Issue Area', 'People Impacted', 'Collaborations']

df_org.columns = ['Slug', 'Status', 'Website', 'Instagram', 'Twitter', 'FaceBook', 'Newsletter', 'Title', 'IRS Standing', 'Zipcode', 'Volunteer', 'Summary', 'Category']
df_23 = df_23.drop(['Ranking'], axis=1)


#df_23 = df_23.fillna('Working Individually')
df_23['Collaborations'].fillna('Working Individually', inplace=True)
df_org = df_org.fillna('N/A')
df_23['People Impacted'].fillna('Not Applicable', inplace=True) #Missing 2 values for this category

print(df_23.info())


def extract_direct_impact(text):
    match = re.search(r'Direct Impact: ([\d,]+\.?\d*)', text)
    if match:
        return float(match.group(1).replace(',', ''))  # Remove commas and convert to float
    return None

df_23['People Impacted'] = df_23['People Impacted'].apply(extract_direct_impact)
df_org = df_org.drop_duplicates(subset='Title')
final_List= df_23.merge(df_org , left_on='Organization', right_on= 'Title', how='inner')
final_List = final_List.drop(['Slug_y', 'Title_y'],axis = 1)
final_List = final_List.fillna(0)


print(df_23[['Stage of Innovation', 'Issue Understanding']].head(10))


df_23.to_csv('output_data_23.csv', index=False)