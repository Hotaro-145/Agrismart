import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

# Explicitly locate .env in the exact same directory as config.py
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Validate credentials before passing to Supabase client
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        f"\n\n❌ Critical Error: Could not read credentials from {ENV_PATH}\n"
        f"SUPABASE_URL: {SUPABASE_URL}\n"
        f"SUPABASE_KEY: {'Found' if SUPABASE_KEY else 'Missing'}\n"
        "Please ensure .env exists in /home/houtouro/Programming/backend/\n"
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)