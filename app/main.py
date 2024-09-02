
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.scraper import Scraper
from app.config import Settings
from app.models import ScrapeRequest, ScrapeResponse

app = FastAPI()

settings = Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate(token: str = Depends(oauth2_scheme)):
    if token != settings.static_token:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/scrape", response_model=ScrapeResponse)
async def scrape(request: ScrapeRequest, token: str = Depends(authenticate)):
    scraper = Scraper(request)
    scraped_data = scraper.run()
    return ScrapeResponse(
        status="Success",
        message=f"Scraped {len(scraped_data)} products from {request.pages_limit} pages."
    )
