from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    tg_id: int


class Book(BaseModel):
    book: str
    tg_id: int


@app.get("/")
async def root() -> dict:
    """Root test example

    Returns:
        dict: hello message
    """
    return {"message": "Welcome to book recommendation system"}


@app.get("/recommend")
async def recommend(book_description: Book):
    """_summary_

    Returns:
        _type_: _description_
    """

    return {"message": "recommend"}
