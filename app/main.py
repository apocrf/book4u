from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """_summary_

    Returns:
        _type_: _description_
    """
    return {"message": "Welcome to book recommendation system"}
