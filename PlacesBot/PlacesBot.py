import os
import csv
from apify_client import ApifyClient
import time
import requests

# Get the API key from environment variables
api_key = os.getenv("APIFY_API_TOKEN")

if not api_key:
    raise ValueError("APIFY_API_TOKEN environment variable not set. Please set it before running the script.")

# Initialize the API client
client = ApifyClient(api_key)

ACTOR_ID = "compass~crawler-google-places"

payload = {
    "searchStringsArray": ["restaurants", "salons"],
    "locationQuery": "Lahore, Punjab, Pakistan",
    "maxCrawledPlacesPerSearch": 200,
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

print("Starting extraction via Apify REST API...")

response = requests.post(
    f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs",
    headers=headers,
    json=payload
)
response.raise_for_status()

run_info = response.json()["data"]
run_id = run_info["id"]
dataset_id = run_info["defaultDatasetId"]

print(f"Run started (ID: {run_id}). Waiting for completion...")

while True:
    status_response = requests.get(
        f"https://api.apify.com/v2/actor-runs/{run_id}",
        headers=headers
    )
    status_response.raise_for_status()
    current_status = status_response.json()["data"]["status"]

    if current_status in ["SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"]:
        break

    print(f"Status: {current_status}... waiting 10 seconds.")
    time.sleep(10)

if current_status != "SUCCEEDED":
    print(f"Extraction failed. Final status: {current_status}")
    exit()

print("Run succeeded! Fetching dataset...")

dataset_response = requests.get(
    f"https://api.apify.com/v2/datasets/{dataset_id}/items",
    headers=headers
)
dataset_response.raise_for_status()
raw_items = dataset_response.json()

filtered_leads = []
print("Processing dataset against criteria...")

for item in raw_items:
    raw_reviews = item.get("reviewsCount")
    reviews_count = int(raw_reviews) if raw_reviews is not None else 0

    raw_rating = item.get("totalScore")
    rating = float(raw_rating) if raw_rating is not None else 0.0

    image_urls = item.get("imageUrls")
    has_photos = len(image_urls) > 0 if image_urls is not None else False

    phone = item.get("phoneUnformatted") or item.get("phone")
    website = item.get("website")

    if reviews_count > 100 and rating > 3.5 and has_photos:
        if not website and phone:
            filtered_leads.append({
                "Business Name": item.get("title", "Unknown"),
                "Rating": rating,
                "Total Reviews": reviews_count,
                "Phone Number": phone,
                "Maps URL": item.get("url", "")
            })

print(f"Filtering complete. Found {len(filtered_leads)} leads.")

if filtered_leads:
    csv_filename = "qualified_local_leads.csv"
    csv_headers = ["Business Name", "Rating", "Total Reviews", "Phone Number", "Maps URL"]

    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=csv_headers)
        writer.writeheader()
        writer.writerows(filtered_leads)
        print(f"Saved to '{csv_filename}'.")
else:
    print("No businesses met the criteria.")