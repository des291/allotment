from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client, Client
import os

# Load environment variables from .env
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

response = supabase.table("plots").select("*").execute()
print(f"Response: {response}")
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "Allotment App"}
