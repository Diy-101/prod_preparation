from fastapi import FastAPI
import uvicorn

app = FastAPI()

countries = []

@app.get("/api/ping", tags=['start'])
def ping():
    return {"ok": True}

@app.get("/api/countries", tags=["start"], summary="Get all countries from database")
def get_countries():
    return countries

@app.post("/api/countries/{alpha2}", tags=["start"], summary="Add one schemas to database")
def add_country(name: str):
    countries.append(name)
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)