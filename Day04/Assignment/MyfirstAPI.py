from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Hello from FastAPI!"
    }


@app.get("/about")
def about():
    return {
        "application": "Basic FastAPI API",
        "python": "3.11"
    }