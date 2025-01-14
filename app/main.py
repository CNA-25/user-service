from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return { "Hello": "user-service", "v": "0.1" }
