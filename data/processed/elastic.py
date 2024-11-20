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
git_url = './Combined_data_13_24.csv'
data = pd.read_csv(git_url)

# Define the Elasticsearch index
index_name = "document_index"

# Helper function to check and exclude "Not Applicable", "N/A", "n/a", or NaN
def filter_value(value):
    if pd.isna(value):  # Check if the value is NaN
        return None
    if isinstance(value, str) and value.strip().lower() in ["not applicable", "n/a", "na"]:
        return None
    return value

# Prepare documents for indexing
documents = []
for _, row in data.iterrows():
    # Concatenate fields without headers, excluding filtered values
    basic_text = " ".join(
        filter_value(str(row.get(col, ""))) 
        for col in [
            "Title", "Slug", "Year", "Organization", "Summary", "Goal",
             "Problem Statement", "Impact on LA",
            "Evidence of Success", "Project Description", "Impact Metrics",
            "People Impacted", "Collaborations", "Status", "Mission Statement",
            "Category", "Working Areas in LA"
        ]
        if filter_value(str(row.get(col, "")))
    )
    
    # Concatenate fields with headers, excluding filtered values
    detailed_text = " ".join(
        f"{'Phase' if col == 'Stage of Innovation' else col}: {filter_value(row.get(col, ''))}" 
        for col in ["Ranking", "Website", "Instagram", "Twitter", "FaceBook", "Newsletter", "IRS Standing", "Stage of Innovation"]
        if col != "Stage of Innovation" or filter_value(row.get(col, "")).strip().lower() != "other"  # Exclude "Phase" if value is "other"
    )
    
    
    # Combine the two texts
    organization_text = f"{basic_text} {detailed_text}".strip()
    
    # Create document with single text field
    if organization_text:  # Ensure we don't index empty documents
        document = {
            "_index": index_name,
            "_source": {
                "OrganizationText": organization_text
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
output_path = "13-24data.json"
with open(output_path, 'w') as f:
    json.dump([doc["_source"] for doc in documents], f, indent=4)
print(f"All data saved to {output_path}.")
