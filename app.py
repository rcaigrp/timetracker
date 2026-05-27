import os
import json
from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()
SETTINGS_FILE = "settings.json"
os.makedirs(os.path.dirname(os.path.abspath(SETTINGS_FILE)), exist_ok=True)

def secure_write_settings(data):
    # Atomic write for safety
    temp_file = SETTINGS_FILE + '.tmp'
    with open(temp_file, 'w') as f:
        json.dump(data, f)
    os.chmod(temp_file, 0o600) # Secure permissions
    os.replace(temp_file, SETTINGS_FILE)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        return json.load(open(SETTINGS_FILE))
    return {}

@app.post("/api/settings")
def manage_settings(payload: dict):
    if not all(k in payload for k in ['jira_url', 'username', 'api_key']):
        raise HTTPException(status_code=400, detail="Missing credentials")
    
    # Securely write
    secure_write_settings(payload)
    return {"status": "saved"}

@app.get("/api/projects")
async def fetch_projects():
    settings = load_settings()
    
    if not settings.get('jira_url') or not settings.get('api_key'):
        raise HTTPException(status_code=400, detail="Settings not configured")

    async with httpx.AsyncClient() as client:
        # Retry logic for rate limits (simplified)
        try:
            response = await client.get(
                f"{settings['jira_url']}/rest/api/3/search",
                headers={
                    "Authorization": f"Basic {settings['api_key']}",
                    "Accept": "application/json"
                },
                timeout=10.0 # Timeout for connection
            )
            
            if response.status_code == 401:
                raise HTTPException(status_code=401, detail="Invalid Jira credentials")
            
            return response.json()
            
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=str(e))
