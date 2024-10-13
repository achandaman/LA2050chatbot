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



df_22.columns = ['Title', 'Slug','Year', 'Organization', 'Summary', 'Goal','Ranking', 'Mission Statement', 'Quota', 'Project', 'Support Statement','Impact','End Goal' ,'Location','Progression', 'Collaborations','Companies']
df.columns = ['Title', 'Slug', 'Year', 'Organization', 'Summary', 'Goal', 'Ranking', 'Progression', 'Mission Statement', 'End Goal', 'Quota', 'Support Statement', 'Project', 'Impact', 'Collaborations']
df_org.columns = ['Slug', 'Status', 'Website', 'Instagram', 'Twitter', 'FaceBook', 'Newsletter', 'Title', 'IRS Standing', 'Zipcode', 'Volunteer', 'Summary', 'Category']
df = df.drop(['Ranking'], axis=1)
df_22 = df_22.drop(['Ranking'], axis = 1)
df_22['Collaborations'] = df_22['Collaborations'].fillna('Working Individually')
df_22 = df_22.fillna('N/A')
df = df.fillna('Working Individually')
df_org = df_org.fillna('N/A')
df_org.replace("", "N/A", inplace = True)
def extract_direct_impact(text):
    match = re.search(r'Direct Impact: ([\d,]+\.?\d*)', text)
    if match:
        return float(match.group(1).replace(',', ''))  # Remove commas and convert to float
    return None

df['Impact'] = df['Impact'].apply(extract_direct_impact)
df_22['Impact'] = df_22['Impact'].apply(extract_direct_impact)

df_org = df_org.drop_duplicates(subset='Title')
final_List= df.merge(df_org , left_on='Organization', right_on= 'Title', how='inner')
final_List = final_List.drop(['Slug_y', 'Title_y'],axis = 1)
final_List.replace(" ", "N/A", inplace=True)  
final_List['Impact'] = final_List['Impact'].fillna(0)
print(final_List.head())
final_List_22 = df_22.merge(df_org, left_on='Organization', right_on='Title', how='inner')
final_List_22 = final_List_22.drop(['Slug_y', 'Title_y'], axis=1)
final_List_22.replace(" ", "N/A", inplace=True)
final_List_22['Impact'] = final_List_22['Impact'].fillna(0)
print(final_List_22.head())
combined_df = pd.concat([final_List, final_List_22], ignore_index=True)
combined_output_path = r'C:\Users\Andrew\hello\combined_data.csv'
combined_df.to_csv(combined_output_path, index=False)