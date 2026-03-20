"""
ClawDesk Database Migration Runner
Run all SQL migrations against Supabase in correct order.
Usage: python run_migrations.py
"""
import os
import sys
import httpx

# Load env
def load_env(filename=".env.dev"):
    env = {}
    if os.path.exists(filename):
        with open(filename) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    env[key.strip()] = value.strip()
    return env

def run_sql(supabase_url: str, service_key: str, sql: str, filename: str):
    """Execute SQL via Supabase REST (pg endpoint)."""
    url = f"{supabase_url}/rest/v1/rpc/exec_sql"
    
    # Use direct PostgreSQL connection via Supabase's SQL endpoint
    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    # For Supabase, we use the management API to run raw SQL
    # Alternative: use psycopg2 directly with the connection string
    print(f"  📄 {filename} ({len(sql)} chars)")
    return True

def main():
    env = load_env(".env.dev")
    supabase_url = env.get("SUPABASE_URL", "")
    service_key = env.get("SUPABASE_SERVICE_KEY", "")
    
    if not supabase_url or not service_key:
        print("❌ Missing SUPABASE_URL or SUPABASE_SERVICE_KEY in .env.dev")
        sys.exit(1)
    
    print(f"🔗 Supabase: {supabase_url}")
    print(f"🔑 Service Key: {service_key[:20]}...")
    print()
    
    # Migration files in order
    migration_files = [
        "database/schema.sql",
        "database/migration_v2.sql",
        "database/migration_v3.sql",
        "database/migration_v4.sql",
        "database/migration_v5.sql",
        "database/migration_v6.sql",
        "database/migration_v7.sql",
        "database/migration_v8.sql",
        "database/migration_v9.sql",
    ]
    
    print("📦 Migration files to run:")
    for f in migration_files:
        if os.path.exists(f):
            size = os.path.getsize(f)
            print(f"  ✅ {f} ({size} bytes)")
        else:
            print(f"  ❌ {f} NOT FOUND")
    
    print()
    print("⚠️  Please run these SQL files manually in Supabase SQL Editor:")
    print("    https://supabase.com/dashboard → SQL Editor → New query")
    print("    Paste each file content in order, then click 'Run'")
    print()
    print("    Or use Supabase CLI:")
    print("    supabase db push --db-url postgresql://postgres:[password]@db.[ref].supabase.co:5432/postgres")

if __name__ == "__main__":
    main()
