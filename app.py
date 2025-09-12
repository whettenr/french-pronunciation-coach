from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.routes import router
import pathlib
import uvicorn

app = FastAPI(title="French Pronunciation Tutor API")

# Include your API router
app.include_router(router)



app.mount("/static", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
def index():
    return FileResponse(path=pathlib.Path("frontend/index.html"))


# Entry point
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",   # accessible on local network
        port=8000,
        reload=True       # auto-reload on code changes
    )