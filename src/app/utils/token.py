from itsdangerous.url_safe import URLSafeSerializer
from app.config import auth_settings


tokens = URLSafeSerializer(f"{auth_settings.access_secret_key}")


def gen_token(data: str):
    toks = tokens.dumps(data)

    return toks


def retrieve_token(token: str):
    data = tokens.loads(token)

    return data
