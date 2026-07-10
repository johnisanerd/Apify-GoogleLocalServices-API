"""
Google Local Services API: A Quick Start Example
See more at: https://apify.com/johnvc/google-local-services-api?fpr=9n7kx3
Input schema: https://apify.com/johnvc/google-local-services-api/input-schema?fpr=9n7kx3

This script shows how to call the Google Local Services API on Apify from Python and read
its structured JSON output. It exercises several input parameters so you can see
what is configurable, while keeping the run small so your first call stays cheap.

Get your free Apify API key at: https://apify.com?fpr=9n7kx3
"""

import os
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

# Initialize the Apify client with your API token (read from .env)
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Build the Actor input. Values are kept small to keep this first run cheap.
run_input = {
    # A service to search for. Google supports a fixed set of about 110
    # service types (for example "plumber", "electrician", "hvac", "roofer").
    "queries": ["hvac"],
    # A US city or district. It is resolved internally to the Google place ID.
    "location": "Phoenix, AZ",
    # Advanced: pass a Google place CID directly to skip the location lookup
    # (and its small resolution fee). Every result row includes "dataCid",
    # so you can copy it from a previous run to keep repeat runs cheap.
    # "dataCid": "6745062158417646970",
    # Keep the first run small and cheap: cap the businesses returned.
    "maxResultsPerQuery": 5,
}

# Run the Actor and wait for it to finish
run = client.actor("johnvc/google-local-services-api").call(run_input=run_input)
if run is None:
    raise SystemExit("The Actor run did not return a result.")

# Read structured results from the run's default dataset
# (apify-client 3.x returns a Run object; use .default_dataset_id)
items = list(client.dataset(run.default_dataset_id).iterate_items())
print(f"Returned {len(items)} item(s).\n")

for item in items:
    print(item.get("businessName"),
          "|", item.get("badge"),
          "|", item.get("rating"), "stars",
          "(", item.get("reviews"), "reviews )",
          "|", item.get("phone"))
