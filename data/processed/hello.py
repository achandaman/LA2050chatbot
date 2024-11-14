import pandas as pd
import json
import re
import matplotlib.pyplot as plt
import os
from elasticsearch import Elasticsearch
from IPython.display import display
# Get the directory where the current script is located
base_dir = os.path.dirname(os.path.abspath(__file__))
stage_mapping = {
    'Expansion of Existing Work': [
        'Expand existing project, program, or initiative (expanding and continuing ongoing, successful work)',
        'Expand existing project, program, or initiative',
        'Expand existing program',
        'Expand existing program (expanding and continuing ongoing successful projects)',
        'Expand a pilot or a program'
    ],
    'New or Pilot Projects': [
        'Pilot or new project, program, or initiative (testing or implementing a new idea)',
        'Pilot or new project, program, or initiative',
        'Pilot project or new program',
        'Pilot project (testing a new idea on a small scale to prove feasibility)',
        'Implement a pilot or new project'
    ],
    'Proven Solutions Applied to New Areas': [
        'Applying a proven model or solution to a new issue or sector (e.g., using a job recruiting software or strategy to match clients to supportive housing sites, applying demonstrated strategies from advocating for college affordability to advocating for housing affordability and homelessness, etc.)',
        'Applying a proven solution to a new issue or sector (using an existing model, tool, resource, strategy, etc. for a new purpose)',
        'Applying a proven model or solution to a new issue or sector (e.g, using a job recruiting software or strategy to match clients to supportive housing sites, applying demonstrated strategies from advocating for college affordability to advocating for housing affordability and homelessness, etc.)',
        'Lateral application (testing feasibility of a proven action/solution to a new issue or sector)'
    ],
    'Research and Feasibility': [
        'Research (initial work to identify and understand the problem)',
        'Research (identifying / understanding the problem)',
        'Post-pilot (testing an expansion of concept after initially successful pilot)',
        'Conduct research'
    ],
    'Engagement and Stakeholder Involvement' :[
        'Engage residents and stakeholders'
    ],
    'Educational Enhancement and Learning Experiences': [
        'Enhance student learning by providing them with an engaging learning experiences and hands on activities'
        ]
}
# Construct file paths relative to the script's location
org_data_path = './data/organizations-new.json'
data_2013_path = './data/idea-2013-new.json'
data_2014_path = './data/idea-2014-new.json'
data_2015_path = './data/idea-2015-new.json'
data_2016_path = './data/idea-2016-new.json'
data_2018_path = './data/idea-2018-new.json'
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
df_13 = load_json_to_df(data_2013_path)
df_14 = load_json_to_df(data_2014_path)
df_15 = load_json_to_df(data_2015_path)
df_16 = load_json_to_df(data_2016_path)
df_18 = load_json_to_df(data_2018_path)
df_19 = load_json_to_df(data_2019_path)
df_20 = load_json_to_df(data_2020_path)
df_21 = load_json_to_df(data_2021_path)
df_22 = load_json_to_df(data_2022_path)
df_23 = load_json_to_df(data_2023_path)
df_24 = load_json_to_df(data_2024_path)

print(df_13.columns)
df_13.columns = ['Title', 'Slug', 'Year', 'Organization', 'Summary', 'Goal', 'Ranking',
                 'Project Description','Problem Statement','Collaborations','Impact on LA', 'Evidence of Success']
df_13['Goal'] = df_13['Goal'].fillna('Not Applicable')

df_14 = df_14.rename(columns={
    'title': 'Title',
    'slug': 'Slug',
    'yearSubmitted': 'Year',
    'organization': 'Organization',
    'summary': 'Summary',
    'goal': 'Goal',
    'projectRanking': 'Ranking',
    'What will you do to implement this idea/project?': 'Problem Statement',
    'How will your idea/project help make LA the best place to LEARN today? In 2050?': 'Learn Impact',
    'Which area(s) of LA does your project benefit?': 'Working Areas in LA',
    'What is your idea/project in more detail?': 'Project Description',
    'How will your project impact the LA2050 LEARN metrics?': 'Learn Metrics',
    'What resources does your project need?': 'Valuable Resources',
    'How will your idea/project help make LA the best place to LIVE today? In 2050?': 'Live Impact',
    'How will your project impact the LA2050 LIVE metrics?': 'Live Metrics',
    'How will your idea/project help make LA the best place to CONNECT today? In 2050?': 'Connect Impact',
    'How will your project impact the LA2050 CONNECT metrics?': 'Connect Metrics',
    'How will your idea/project help make LA the best place to PLAY today? In 2050?': 'Play Impact',
    'How will your project impact the LA2050 PLAY metrics?': 'Play Metrics',
    'How will your idea/project help make LA the best place to CREATE today? In 2050?': 'Create Impact',
    'How will your project impact the LA2050 CREATE metrics?': 'Create Metrics',
    'Please explain how you will evaluate your project.': 'Evidence of Success',
    'Please identify any partners or collaborators who will work with you on this project.': 'Collaborations'
})
df_14['Impact Metrics'] = df_14[['Play Metrics', 'Live Metrics', 'Connect Metrics', 'Create Metrics', 'Learn Metrics']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_14.drop(['Play Metrics', 'Live Metrics', 'Connect Metrics', 'Create Metrics', 'Learn Metrics', 'Does your project impact Los Angeles County?', 'What two lessons have informed your solution or project?',
            'Please list at least two major barriers/challenges you anticipate. What is your strategy for ensuring a successful implementation?',
            'Please describe yourself.','Explain how implementing your project within the next twelve months is an achievable goal.','Whom will your project benefit?',
             'In one sentence, please describe your idea or project.','Please elaborate on how your project will impact the above metrics.'], axis=1, inplace=True)

df_14['Impact on LA'] = df_14[['Live Impact','Connect Impact', 'Create Impact', 'Learn Impact', 'Play Impact']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_14.drop([ 'Live Impact','Connect Impact', 'Create Impact', 'Learn Impact', 'Play Impact'], axis=1, inplace=True)
df_14['Impact on LA'] = df_14['Impact on LA'].replace("", "Not Applicable")

df_15.columns = [
    'Title', 'Slug', 'Year', 'Organization', 'Summary', 'Goal', 'Ranking',
    'Learn Impact', 'Working Areas in LA', 'Stage of Innovation', 'Evidence of Success',
    'Learn Metrics', 'Valuable Resources', 'Live Metrics', 'Connect Metrics',
    'Connect Impact', 'Play Impact', 'Play Metrics', 'Create Metrics',
    'Create Impact'
]
df_16.columns = [
    'Title', 'Slug', 'Year', 'Organization', 'Summary', 'Goal', 'Ranking',
    'Project Description', 'Create Impact', 'Evidence of Success', 'Valuable Resources',
    'Create Metrics', 'Working Areas in LA', 'Collaborations', 'Learn Impact',
    'Learn Metrics', 'Connect Impact', 'Connect Metrics', 'Live Metrics',
    'Live Impact', 'Play Metrics', 'Play Impact'
]
df_18.columns = ['Title','Slug','Year', 'Organization','Summary','Goal','Ranking',
    'Problem Statement', 'Engagement on Live','Evidence of Success','Project Description',
    'Live Impact Details','Live Metrics','Additional Goals', 'Working Areas in LA',
    'Future Goals', 'Connect Metrics', 'Engagement on Connect', 'Connect Impact Details',
    'Create Metrics','Create Impact Details','Engagement on Create', 'Engagement on Learn',
    'Learn Metrics','Learn Impact Details','Play Metrics','Engagement on Play','Play Impact Details'
    ]
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

df_15['Impact Metrics'] = df_15[['Play Metrics', 'Live Metrics', 'Connect Metrics', 'Create Metrics', 'Learn Metrics']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_15.drop(['Play Metrics', 'Live Metrics', 'Connect Metrics', 'Create Metrics', 'Learn Metrics'], axis=1, inplace=True)

df_15['Impact on LA'] = df_15[['Connect Impact', 'Create Impact', 'Learn Impact', 'Play Impact']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_15.drop([ 'Connect Impact', 'Create Impact', 'Learn Impact', 'Play Impact'], axis=1, inplace=True)
df_15['Impact on LA'] = df_15['Impact on LA'].replace("", "Not Applicable")

df_16['Impact Metrics'] = df_16[['Play Metrics', 'Live Metrics', 'Connect Metrics', 'Create Metrics', 'Learn Metrics']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_16.drop(['Play Metrics', 'Live Metrics', 'Connect Metrics', 'Create Metrics', 'Learn Metrics'], axis=1, inplace=True)

df_16['Impact on LA'] = df_16[['Live Impact', 'Connect Impact', 'Create Impact', 'Learn Impact', 'Play Impact']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_16.drop(['Live Impact', 'Connect Impact', 'Create Impact', 'Learn Impact', 'Play Impact'], axis=1, inplace=True)
df_16['Collaborations'] = df_16['Collaborations'].fillna('Working Individually')

df_18['Live Impact Detail'] = df_18[['Live Impact Details', 'Engagement on Live']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_18.drop(['Live Impact Details', 'Engagement on Live'], axis=1, inplace=True)

df_18['Connect Impact Detail'] = df_18[['Connect Impact Details', 'Engagement on Connect']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_18.drop(['Connect Impact Details', 'Engagement on Connect'], axis=1, inplace=True)

df_18['Create Impact Detail'] = df_18[['Create Impact Details', 'Engagement on Create']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_18.drop(['Create Impact Details', 'Engagement on Create'], axis=1, inplace=True)

df_18['Learn Impact Detail'] = df_18[['Learn Impact Details', 'Engagement on Learn']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_18.drop(['Learn Impact Details', 'Engagement on Learn'], axis=1, inplace=True)

df_18['Play Impact Detail'] = df_18[['Play Impact Details', 'Engagement on Play']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_18.drop(['Play Impact Details', 'Engagement on Play'], axis=1, inplace=True)

df_18['Impact Metrics'] = df_18[['Play Metrics', 'Live Metrics', 'Connect Metrics', 'Create Metrics', 'Learn Metrics']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_18.drop(['Play Metrics', 'Live Metrics', 'Connect Metrics', 'Create Metrics', 'Learn Metrics'], axis=1, inplace=True)

df_18['Impact on LA'] = df_18[['Live Impact Detail', 'Connect Impact Detail', 'Create Impact Detail', 'Learn Impact Detail', 'Play Impact Detail']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_18.drop(['Live Impact Detail', 'Connect Impact Detail', 'Create Impact Detail', 'Learn Impact Detail', 'Play Impact Detail'], axis=1, inplace=True)

# Combine the metric columns into one "Impact Metrics" column
df_19['Impact Metrics'] = df_19[['Play Metrics', 'Live Metrics', 'Connect Metrics','Create Metrics', 'Learn Metrics']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_19.drop(['Live Metrics', 'Connect Metrics', 'Learn Metrics', 'Play Metrics', 'Create Metrics'], axis=1, inplace=True)
df_19['Impact on LA'] = df_19[['Play Impact','Connect Impact','Create Impact','Learn Impact', 'Live Impact']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_19.drop(['Play Impact','Connect Impact','Create Impact','Learn Impact', 'Live Impact'], axis=1, inplace=True)

df_20['People Impacted'] = df_20['People Impacted'].astype(str) + "" + df_20['Impacted People1'].astype(str)
df_20['Project Description'] = df_20['Project Description'].astype(str) + "" + df_20['Org Importance1'].astype(str)
df_20 = df_20.drop(columns=['Impacted People1', 'Org Importance1'])
df_20['Impact Metrics'] = df_20[['Live Metrics', 'Connect Metrics','Play Metrics', 'Learn Metrics', 'Create Metrics']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_20.drop(['Live Metrics', 'Connect Metrics', 'Learn Metrics', 'Create Metrics','Play Metrics'], axis=1, inplace=True)

df_21['Impact Metrics'] = df_21[['Live Metrics', 'Connect Metrics', 'Learn Metrics', 'Play Metrics', 'Create Metrics']].apply(lambda x: ', '.join(x.dropna()), axis=1)
df_21.drop(['Live Metrics', 'Connect Metrics', 'Learn Metrics', 'Play Metrics', 'Create Metrics'], axis=1, inplace=True)

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
final_list_18 = merge_dataframes(df_18, df_org)
final_list_16 = merge_dataframes(df_16, df_org)
final_list_15 = merge_dataframes(df_15, df_org)
final_list_14 = merge_dataframes(df_14,df_org)
final_list_13 = merge_dataframes(df_13,df_org)

combined_df = pd.concat([final_list, final_list_22, final_list_21, final_list_20, final_list_19, final_list_18,final_list_16,final_list_15,final_list_14,final_list_13], ignore_index=True)

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

def map_stage_individual(stage, mapping):
    """Maps each 'Stage of Innovation' entry to a standardized category based on the stage_mapping dictionary."""
    for key, values in mapping.items():
        if stage.strip() in values:  # Strip any leading/trailing whitespace for matching
            return key
    return 'Other'

combined_df['Stage of Innovation'] = combined_df['Stage of Innovation'].apply(map_stage_individual, mapping=stage_mapping)
combined_df['Goal'] = combined_df['Goal'].str.replace(r'\s\|\sWorking Individually', '', regex=True)
# Step 1: Sort each combination alphabetically for consistent ordering
combined_df['Goal'] = combined_df['Goal'].apply(lambda x: ' | '.join(sorted(x.split(' | '))))
combined_df['Goal'] = combined_df['Goal'].apply(lambda x: x.split(' | ')[0] if len(set(x.split(' | '))) == 1 else x)

combined_df.drop(['Future Goals','COVID-19 Impact'],axis=1, inplace=True)
# Save the modified DataFrame to a CSV file
combined_df.to_csv('combined_data_with_consolidation.csv', index=False)
print(combined_df.columns)
