from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/api/ping")
def ping():
    return {"status": "success"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)