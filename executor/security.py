import os

TOKEN = os.environ.get("NOUS_TOKEN", "")

def check_token(request):
    if not TOKEN:
        return True
    return request.headers.get("X-NOUS-TOKEN") == TOKEN
