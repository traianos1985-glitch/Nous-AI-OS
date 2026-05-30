import os

from executor.api_tokens import token_allowed

TOKEN = os.environ.get("NOUS_TOKEN", "")


def check_token(request):
    header_token = request.headers.get("X-NOUS-TOKEN", "")

    if TOKEN and header_token == TOKEN:
        return True

    if token_allowed(header_token):
        return True

    if not TOKEN:
        return True

    return False
