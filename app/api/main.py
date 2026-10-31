import string
import secrets
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

class ShortenRequest(BaseModel):
    url: HttpUrl

class ShortenResponse(BaseModel):
    code: str
    short_url: HttpUrl

alphabet = string.ascii_letters + string.digits

app = FastAPI(
    title="urlshort",
    description="A simple url shortener backend API",
    version="1.0.0"
)

# code, full url
stored_urls: dict[str, str] = {}

@app.get("/health")
def get_health() -> str:
    return "ok"

@app.get("/{code}")
async def get_code(code: str):
    url = stored_urls.get(code)
    
    if url is not None:
        return RedirectResponse(url=url)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Code not found"
    )

@app.post("/shorten", status_code=status.HTTP_201_CREATED, response_model=ShortenResponse)
async def post_url(shorten_request: ShortenRequest, request: Request) -> ShortenResponse:
    url = str(shorten_request.url)
    code = generate_code()
    
    stored_urls[code] = url
    
    short_url = str(request.base_url) + code
    
    return {
        "code": code, 
        "short_url": short_url
    }
    


def generate_code() -> str:
    while True:
        code = ''.join(secrets.choice(alphabet) for i in range(10))
        if stored_urls.get(code) is None:
            return code
    