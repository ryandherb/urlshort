from pydantic import BaseModel, HttpUrl
from fastapi import status

class ShortenRequest(BaseModel):
    url: HttpUrl

class ShortenResponse(BaseModel):
    code: str
    short_url: HttpUrl