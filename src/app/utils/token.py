from itsdangerous.url_safe import URLSafeSerializer
from src.app.config import auth_settings
from itsdangerous.exc import BadSignature

tokens = URLSafeSerializer(f"{auth_settings.access_secret_key}")


def gen_token(data: str):

    toks = tokens.dumps(data)

    return toks


def retrieve_token(token: str):
    try:
        data = tokens.loads(token)
    except BadSignature:
        return None
    return data
