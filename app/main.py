from fastapi import FastAPI
import uvicorn
from app.routes import router

app = FastAPI(
    title="Summary API",
    description="An API to generate summaries from text inputs.",
    version="0.1.0",
)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
