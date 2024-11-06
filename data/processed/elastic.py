import os
import pandas as pd
import json
from elasticsearch import Elasticsearch, helpers

# Elasticsearch connection setup
es_client = Elasticsearch(
    "http://localhost:9200",
    basic_auth=('elastic', '123456')  # Using basic_auth for authentication
)

# Step 1: Load the dataset from GitHub
git_url = 'https://raw.githubusercontent.com/achandaman/LA2050chatbot/refs/heads/main/data/processed/combined_data_with_consolidation.csv'
data = pd.read_csv(git_url)

# Define the Elasticsearch index
index_name = "document_index"

# Prepare documents for indexing
documents = []
for _, row in data.iterrows():
    document = {
        "_index": index_name,
        "_source": {
            "Title": row.get("Title", ""),
            "Slug": row.get("Slug", ""),
            "Year": int(row.get("Year", 0)),
            "Organization": row.get("Organization", ""),
            "Summary": row.get("Summary", ""),
            "Goal": row.get("Goal", ""),
            "Ranking": row.get("Ranking", ""),
            "Stage of Innovation": row.get("Stage of Innovation", ""),
            "Problem Statement": row.get("Problem Statement", ""),
            "Impact on LA": row.get("Impact on LA", ""),
            "Evidence of Success": row.get("Evidence of Success", ""),
            "Project Description": row.get("Project Description", ""),
            "Impact Metrics": row.get("Impact Metrics", ""),
            "People Impacted": row.get("People Impacted", ""),
            "Collaborations": row.get("Collaborations", ""),
            "Status": row.get("Status", ""),
            "Website": row.get("Website", ""),
            "Instagram": row.get("Instagram", ""),
            "Twitter": row.get("Twitter", ""),
            "FaceBook": row.get("FaceBook", ""),
            "Newsletter": row.get("Newsletter", ""),
            "IRS Standing": row.get("IRS Standing", ""),
            "Zipcode": row.get("Zipcode", ""),
            "Volunteer": row.get("Volunteer", ""),
            "Mission Statement": row.get("Mission Statement", ""),
            "Category": row.get("Category", ""),
            "Working Areas in LA": row.get("Working Areas in LA", ""),
            "Companies": row.get("Companies", ""),
            "Valuable Resources": row.get("Valuable Resources", ""),
            "COVID-19 Impact": row.get("COVID-19 Impact", "")
        }
    }
    documents.append(document)

# Bulk insert with error handling
try:
    success, failed = helpers.bulk(es_client, documents, raise_on_error=False, stats_only=True)
    print(f"{success} documents indexed successfully.")
    if failed:
        print(f"{failed} documents failed to index.")
except helpers.BulkIndexError as e:
    print(f"Error indexing documents: {e}")
    # Optionally, write errors to a log file for detailed analysis
    with open("bulk_index_errors.log", "w") as log_file:
        json.dump(e.errors, log_file, indent=4)
    print("Detailed errors have been logged to bulk_index_errors.log")

# Save data to a single JSON file
output_path = "all_data.json"
with open(output_path, 'w') as f:
    json.dump([doc["_source"] for doc in documents], f, indent=4)
print(f"All data saved to {output_path}.")