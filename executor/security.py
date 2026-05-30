import os

from executor.api_tokens import token_allowed, has_active_tokens

TOKEN = os.environ.get("NOUS_TOKEN", "")


def _header_token(request):
    return request.headers.get("X-NOUS-TOKEN", "")


def check_token(request):
    header_token = _header_token(request)

    if TOKEN and header_token == TOKEN:
        return True

    if token_allowed(header_token):
        return True

    if not TOKEN:
        return True

    return False


def check_admin_token(request):
    header_token = _header_token(request)

    if TOKEN and header_token == TOKEN:
        return True

    if token_allowed(header_token):
        return True

    # Bootstrap mode: allow first token creation only when no env token
    # and no active stored tokens exist.
    if not TOKEN and not has_active_tokens():
        return True

    return False
