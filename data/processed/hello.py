import pandas as pd
import json
import re
import matplotlib.pyplot as plt
import os
from elasticsearch import Elasticsearch
from IPython.display import display
# Get the directory where the current script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct file paths relative to the script's location
org_data_path = './data/organizations-new.json'
data_2019_path = './data/idea-2019-new.json'
data_2020_path = './data/idea-2020-new.json'
data_2021_path = './data/idea-2021-new.json'
data_2022_path = './data/idea-2022-new.json'
data_2023_path = './data/idea-2023-new.json'
data_2024_path = './data/idea-2024-new.json'
def load_json_to_df(file_path):
    with open(file_path, encoding='utf-8') as f:
        return pd.json_normalize(json.load(f))
df_org = load_json_to_df(org_data_path)
df_19 = load_json_to_df(data_2019_path)
df_20 = load_json_to_df(data_2020_path)
df_21 = load_json_to_df(data_2021_path)
df_22 = load_json_to_df(data_2022_path)
df_23 = load_json_to_df(data_2023_path)
df_24 = load_json_to_df(data_2024_path)

df_19.columns = ['Title', 'Slug', 'Year', 'Organization', 'Summary', 'Goal', 'Ranking',
                    'Play Metrics', 'Working Areas in LA', 'Stage of Innovation','Problem Statement',
                     'Play Impact', 'Evidence of Success','Live Impact', 'Live Metrics','Companies'
                    ,'Create Metrics', 'Create Impact','Connect Metrics', 
                    'Connect Impact','Learn Metrics', 'Learn Impact']

df_20.columns = [ 'Title', 'Slug', 'Year', 'Organization', 'Summary', 'Goal', 'Ranking',
                  'People Impacted', 'Play Metrics', 'Additional Goals', 
                  'Stage of Innovation', 'Evidence of Success', 'Valuable Resources', 
                  'Working Areas in LA', 'Collaborations', 'Problem Statement', 
                  'Project Description', 'Impact on LA', 'Learn Metrics',
                  'Live Metrics', 'Create Metrics', 'COVID-19 Impact', 
                  'Companies', 'Connect Metrics',
                  'Impacted People1', 'Org Importance1'
]
df_20['People Impacted'] = df_20['People Impacted'].astype(str) + "" + df_20['Impacted People1'].astype(str)

# Combine 'Project Description' with 'Org Importance1'
df_20['Project Description'] = df_20['Project Description'].astype(str) + "" + df_20['Org Importance1'].astype(str)
df_20 = df_20.drop(columns=['Impacted People1', 'Org Importance1'])
df_21.columns = ['Title', 'Slug', 'Year', 'Organization', 'Summary', 'Goal', 'Ranking', 
                   'Project Description', 'Stage of Innovation', 'Evidence of Success', 
                   'Problem Statement', 'Additional Goals', 'Working Areas in LA', 
                   'Impact on LA', 'People Impacted', 'Live Metrics', 'Connect Metrics', 
                   'Collaborations', 'Learn Metrics', 'Play Metrics', 'Create Metrics']

df_22.columns = ['Title', 'Slug','Year', 'Organization', 'Summary', 'Goal','Ranking', 
                   'Problem Statement', 'Evidence of Success', 'Impact Metrics', 
                   'Project Description','People Impacted','Impact on LA' ,'Working Areas in LA',
                   'Stage of Innovation', 'Collaborations','Companies']
df_23.columns = ['Title', 'Slug', 'Year', 'Organization', 'Summary', 'Goal', 'Ranking',
                 'Issue Understanding','Stage of Innovation', 'Project Description',
                   'Impact on LA', 'Working Areas in LA',  'Evidence of Success',
                   'Primary Issue Area', 'People Impacted', 'Collaborations']
df_24.columns = ['Title', 'Slug', 'Year', 'Organization', 'Summary', 'Goal', 'Ranking',
                   'Stage of Innovation', 'Problem Statement', 'Impact on LA', 
                   'Evidence of Success', 'Project Description', 'Impact Metrics', 
                   'People Impacted', 'Collaborations']

df_org.columns = ['Slug', 'Status', 'Website', 'Instagram', 'Twitter', 'FaceBook', 'Newsletter',
                   'Title', 'IRS Standing', 'Zipcode', 'Volunteer', 'Mission Statement', 'Category']

# Combine the metric columns into one "Impact Metrics" column
df_19['Impact Metrics'] = df_19[['Play Metrics', 'Live Metrics', 'Connect Metrics','Create Metrics', 'Learn Metrics']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_19.drop(['Live Metrics', 'Connect Metrics', 'Learn Metrics', 'Play Metrics', 'Create Metrics'], axis=1, inplace=True)
df_19['Impact on LA'] = df_19[['Play Impact','Connect Impact','Create Impact','Learn Impact', 'Live Impact']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_19.drop(['Play Impact','Connect Impact','Create Impact','Learn Impact', 'Live Impact'], axis=1, inplace=True)

df_21['Impact Metrics'] = df_21[['Live Metrics', 'Connect Metrics', 'Learn Metrics', 'Play Metrics', 'Create Metrics']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_21.drop(['Live Metrics', 'Connect Metrics', 'Learn Metrics', 'Play Metrics', 'Create Metrics'], axis=1, inplace=True)

df_20['Impact Metrics'] = df_20[['Live Metrics', 'Connect Metrics','Play Metrics', 'Learn Metrics', 'Create Metrics']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_20.drop(['Live Metrics', 'Connect Metrics', 'Learn Metrics', 'Create Metrics','Play Metrics'], axis=1, inplace=True)

df_21 = df_21.fillna('Working Individually')
df_21['Collaborations'].fillna('Working Individually')
df_21['People Impacted'].fillna('Not Applicable')
df_22['Collaborations'] = df_22['Collaborations'].fillna('Working Individually')
df_22 = df_22.fillna('Not Applicable')
df_24 = df_24.fillna('Working Individually')
df_org = df_org.fillna('Not Applicable')
df_org.replace("", "Not Applicable", inplace = True)

def extract_direct_impact(text):
    match = re.search(r'Direct Impact: ([\d,]+\.?\d*)', text)
    if match:
        return float(match.group(1).replace(',', ''))  # Remove commas and convert to float
    return None

for df in [df_21, df_22, df_24, df_20]:
    df['People Impacted'] = df['People Impacted'].apply(extract_direct_impact)


df_org = df_org.drop_duplicates(subset='Title')

def merge_dataframes(df1, df2):
    merged = df1.merge(df2, left_on='Organization', right_on='Title', how='inner')
    merged.rename(columns={'Title_x': 'Title', 'Slug_x': 'Slug'}, inplace=True) 
    return merged.drop(['Slug_y', 'Title_y'], axis=1)

final_list = merge_dataframes(df_24, df_org)
final_list_22 = merge_dataframes(df_22, df_org)
final_list_21 = merge_dataframes(df_21, df_org)
final_list_20 =  merge_dataframes(df_20,df_org)
final_list_19 = merge_dataframes(df_19,df_org)
combined_df = pd.concat([final_list, final_list_22, final_list_21, final_list_20, final_list_19], ignore_index=True)

# Fill any irregular values in the combined dataframe
combined_df['Working Areas in LA'] = combined_df['Working Areas in LA'].fillna('Los Angeles')
combined_df['Additional Goals'] = combined_df['Additional Goals'].str.replace('LA is the best place to ', '', regex=False)
combined_df['Additional Goals'] = combined_df['Additional Goals'].str.replace('LA is the healthiest place to ', '', regex=False)
combined_df['Goal'] = combined_df[['Goal', 'Additional Goals']].apply(lambda x: ' | '.join(x.dropna()), axis=1)
combined_df['Companies'] = combined_df['Companies'].fillna('Not Applicable')
combined_df['Collaborations'] = combined_df['Collaborations'].fillna("Working Individually")
combined_df = combined_df.fillna('Not Applicable')

combined_df.drop(['Additional Goals'], axis=1, inplace=True)
combined_df.rename(columns={'Summary_x': 'Summary', 'Summary_y': 'Organization Statement'}, inplace=True) 
# Save the combined dataframe to a CSV file


