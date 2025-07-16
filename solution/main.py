from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/api/ping")
def ping():
    return {"status": "success"}
