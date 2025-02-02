import os
import http.client
import json
from dotenv import load_dotenv
import logfire

logfire.configure(environment=os.getenv("LOGFIRE_ENVIRONMENT"))
load_dotenv()

SERPER_DEV_API_KEY = "d62ad234a40fa876620410c20b79898d1fc56e94"
search_type = "shopping"


def is_google_search(input: str, search_type: str):
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({"q": input, "gl": "vn"})
    headers = {"X-API-KEY": SERPER_DEV_API_KEY, "Content-Type": "application/json"}
    conn.request("POST", f"/{search_type}", payload, headers)
    res = conn.getresponse()
    data = json.load(res)
    logfire.info(str(data))
    context = ""
    if search_type == "search":
        for item in data["organic"]:
            context += f"Title: {item['title']}, context: {item['snippet']}" + "\n"
        return context
    elif search_type == "shopping":
        return data["shopping"]
    return data
