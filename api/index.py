"""
Vercel Serverless Function Entry Point
Wraps FastAPI app for Vercel Python runtime
"""
import os
import sys

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Disable Supabase Realtime WebSocket (blocks in serverless)
os.environ.setdefault("SUPABASE_REALTIME_URL", "")

from server.main import app
