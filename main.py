from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scraper import Scraper
import uvicorn

app = FastAPI()
scraper = Scraper()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/")
async def root():
    return {"message": "root"}


@app.post("/search")
async def getResults(keyword: str):
    return {"data": scraper.getResults(keyword)}


@app.post("/info")
async def getBookInfo(url: str):
    return {"data": scraper.getBookInfo(url)}


@app.post("/images")
async def getImages(url: str):
    return {"data": scraper.getImages(url)}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
