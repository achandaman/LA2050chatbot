import pandas as pd
import json
import re
import matplotlib.pyplot as plt
import os
from elasticsearch import Elasticsearch
from IPython.display import display
def load_json_to_df(file_path):
    with open(file_path, encoding='utf-8') as f:
        return pd.json_normalize(json.load(f))
df_org = load_json_to_df(r'C:\Users\Andrew\Downloads\organizations-new.json')
df = load_json_to_df(r'C:\Users\Andrew\hello\idea-2024-new.json')
df_22 = load_json_to_df(r'C:\Users\Andrew\Downloads\idea-2022-new.json')
df_21 = load_json_to_df(r'C:\Users\Andrew\Downloads\idea-2021-new.json')


df_21.columns = ['Title', 'Slug', 'Year', 'Organization', 'Description', 'Goal', 'Ranking', 
                   'Project Description', 'Stage of Innovation', 'Evidence of Success', 
                   'Problem Statement', 'Additional Goals', 'Working Areas in LA', 
                   'Impact on LA', 'People Impacted', 'Live Metrics', 'Connect Metrics', 
                   'Collaborations', 'Learn Metrics', 'Play Metrics', 'Create Metrics']

df_22.columns = ['Title', 'Slug','Year', 'Organization', 'Description', 'Goal','Ranking', 
                   'Problem Statement', 'Evidence of Success', 'Impact Metrics', 
                   'Project Description','People Impacted','Impact on LA' ,'Working Areas in LA',
                   'Stage of Innovation', 'Collaborations','Companies']

df.columns = ['Title', 'Slug', 'Year', 'Organization', 'Description', 'Goal', 'Ranking',
                   'Stage of Innovation', 'Problem Statement', 'Impact on LA', 
                   'Evidence of Success', 'Project Description', 'Impact Metrics', 
                   'People Impacted', 'Collaborations']

df_org.columns = ['Slug', 'Status', 'Website', 'Instagram', 'Twitter', 'FaceBook', 'Newsletter',
                   'Title', 'IRS Standing', 'Zipcode', 'Volunteer', 'Summary', 'Category']
# Combine the metric columns into one "Impact Metrics" column
df_21['Impact Metrics'] = df_21[['Live Metrics', 'Connect Metrics', 'Learn Metrics', 'Play Metrics', 'Create Metrics']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_21.drop(['Live Metrics', 'Connect Metrics', 'Learn Metrics', 'Play Metrics', 'Create Metrics'], axis=1, inplace=True)

for df in [df_21, df_22, df]:
    df.drop(['Ranking'], axis=1, inplace=True)


df_21 = df_21.fillna('Working Individually')
df_21['Collaborations'].fillna('Working Individually')
df_21['People Impacted'].fillna('Not Applicable')
df_22['Collaborations'] = df_22['Collaborations'].fillna('Working Individually')
df_22 = df_22.fillna('Not Applicable')
df = df.fillna('Working Individually')
df_org = df_org.fillna('N/A')
df_org.replace("", "N/A", inplace = True)

def extract_direct_impact(text):
    match = re.search(r'Direct Impact: ([\d,]+\.?\d*)', text)
    if match:
        return float(match.group(1).replace(',', ''))  # Remove commas and convert to float
    return None

for df in [df_21, df_22, df]:
    df['People Impacted'] = df['People Impacted'].apply(extract_direct_impact).fillna('Not Applicable')


df_org = df_org.drop_duplicates(subset='Title')

def merge_dataframes(df1, df2):
    merged = df1.merge(df2, left_on='Organization', right_on='Title', how='inner')
    merged.rename(columns={'Title_x': 'Title', 'Slug_x': 'Slug'}, inplace=True) 
    return merged.drop(['Slug_y', 'Title_y'], axis=1)

final_list = merge_dataframes(df, df_org)
final_list_22 = merge_dataframes(df_22, df_org)
final_list_21 = merge_dataframes(df_21, df_org)

combined_df = pd.concat([final_list, final_list_22, final_list_21], ignore_index=True)

# Fill any irregular values in the combined dataframe
combined_df['Working Areas in LA'] = combined_df['Working Areas in LA'].fillna('Los Angeles')
combined_df['Additional Goals'] = combined_df['Additional Goals'].str.replace('LA is the best place to ', '', regex=False)
combined_df['Additional Goals'] = combined_df['Additional Goals'].str.replace('LA is the healthiest place to ', '', regex=False)
combined_df['Goal'] = combined_df[['Goal', 'Additional Goals']].apply(lambda x: ' | '.join(x.dropna()), axis=1)
combined_df['Companies'] = combined_df['Companies'].fillna('Not Applicable')
combined_df.fillna('N/A')


combined_df.drop(['Additional Goals'], axis=1, inplace=True)

# Save the combined dataframe to a CSV file
combined_output_path = r'C:\Users\Andrew\hello\combined1_data.csv'
combined_df.to_csv(combined_output_path, index=False)
