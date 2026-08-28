from dotenv import load_dotenv
import os

load_dotenv(".env")

print("ENV EXISTS:", bool(os.getenv("FORTYGUARD_API_KEY")))

from Fortyguard import FortyGuardClient
from Fortyguard.samples import MANHATTAN_POLYGON
client = FortyGuardClient(
    api_key="1f09e84c78a5b65ff648ce9e93b55cc6"
)

response = client.create_heatmap(
    polygon_aoi=MANHATTAN_POLYGON,
    start_date="2024-07-15",
    start_time="14:00",
    filter_type=1,
    granularity=100,
)

print(response)