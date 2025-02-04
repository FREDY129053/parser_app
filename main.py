from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from parser import get_main_wiki_block, get_frequencies

app = FastAPI()


origins = [
    "http://localhost:5173",
    "https://fredy129053.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/proxy")
def read_root(url: str):
  if url == '':
    block = get_main_wiki_block()
    return {"data": get_frequencies(block)}
  
  block = get_main_wiki_block(url)
  return {"data": get_frequencies(block)}